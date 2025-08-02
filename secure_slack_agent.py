import os
import time
import requests
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from datetime import datetime
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Agent Configuration
AGENT_NAME = "Slack AI Agent"
AGENT_LLM = "openai/gpt-4"
AGENT_LLM_SYSTEM_PROMPT = "You are a helpful assistant agent in a Slack channel."
AGENT_LLM_TEMPERATURE = 0.7  # Reduced from 1.0 for more consistent responses
AGENT_LLM_MAX_TOKENS = 1000
AGENT_MAX_HISTORY = 10

# Load configuration from environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Validate required environment variables
required_vars = {
    "SLACK_BOT_TOKEN": SLACK_BOT_TOKEN,
    "SLACK_APP_TOKEN": SLACK_APP_TOKEN,
    "CHANNEL_ID": CHANNEL_ID,
    "OPENROUTER_API_KEY": OPENROUTER_API_KEY
}

missing_vars = [var for var, value in required_vars.items() if not value]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    logger.error("Please create a .env file with these variables")
    exit(1)

# Initialize clients
web_client = WebClient(token=SLACK_BOT_TOKEN)

# Get bot user ID
try:
    bot_info = web_client.auth_test()
    BOT_USER_ID = bot_info["user_id"]
    logger.info(f"✓ Connected to Slack! Bot User ID: {BOT_USER_ID}")
except Exception as e:
    logger.error(f"Failed to connect with bot token: {e}")
    exit(1)

# Initialize socket client
socket_client = SocketModeClient(
    app_token=SLACK_APP_TOKEN,
    web_client=web_client
)

# Store recent conversation history
conversation_history = []

# Track processed messages with cleanup
processed_messages = {}
MESSAGE_DEDUP_WINDOW = 30  # seconds
MAX_PROCESSED_MESSAGES = 1000

def cleanup_old_messages():
    """Clean up old processed messages to prevent memory leaks"""
    current_time = time.time()
    expired_messages = [
        msg_id for msg_id, timestamp in processed_messages.items()
        if current_time - timestamp > MESSAGE_DEDUP_WINDOW
    ]
    for msg_id in expired_messages:
        del processed_messages[msg_id]
    
    # If still too many messages, remove oldest
    if len(processed_messages) > MAX_PROCESSED_MESSAGES:
        sorted_messages = sorted(processed_messages.items(), key=lambda x: x[1])
        for msg_id, _ in sorted_messages[:len(sorted_messages) - MAX_PROCESSED_MESSAGES]:
            del processed_messages[msg_id]

def generate_response(prompt, history=None):
    """Generate response using OpenRouter API with retry logic"""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            messages = [{"role": "system", "content": AGENT_LLM_SYSTEM_PROMPT}]

            # Add conversation history if provided
            if history:
                for h in history[-8:]:  # Last 8 messages for context
                    messages.append({"role": h["role"], "content": h["content"]})

            messages.append({"role": "user", "content": prompt})

            data = {
                "model": AGENT_LLM,
                "messages": messages,
                "temperature": AGENT_LLM_TEMPERATURE,
                "max_tokens": AGENT_LLM_MAX_TOKENS,
            }

            response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=30)
            response.raise_for_status()

            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                logger.warning("No choices in API response")
                return "Sorry, I couldn't generate a response."

        except requests.exceptions.RequestException as e:
            logger.error(f"API request error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
            else:
                return "Sorry, there was an error generating a response."
        except Exception as e:
            logger.error(f"Unexpected error generating response: {e}")
            return "Sorry, there was an error generating a response."

def send_message(channel, text):
    """Send a message to Slack with rate limiting protection"""
    try:
        response = web_client.chat_postMessage(
            channel=channel,
            text=text
        )
        logger.info(f"Message sent successfully")
        return response
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return None

def process_event(client: SocketModeClient, req: SocketModeRequest):
    """Process incoming events with improved error handling"""
    try:
        if req.type == "events_api":
            # Acknowledge the request
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)

            # Get the event
            event = req.payload.get("event", {})
            event_type = event.get("type")

            # Handle message events
            if event_type == "message":
                # Skip bot messages
                if event.get("bot_id") or event.get("user") == BOT_USER_ID:
                    return

                # Skip subtypes (edits, deletes)
                if event.get("subtype"):
                    return

                # Only respond in our channel
                if event.get("channel") != CHANNEL_ID:
                    return

                text = event.get("text", "")
                user = event.get("user", "Unknown")
                ts = event.get("ts", "")

                # Create a unique message identifier
                message_id = f"{user}-{text}-{int(float(ts))}"

                # Clean up old messages periodically
                if len(processed_messages) % 10 == 0:
                    cleanup_old_messages()

                # Skip if we've seen this message recently
                current_time = time.time()
                if message_id in processed_messages:
                    if current_time - processed_messages[message_id] < MESSAGE_DEDUP_WINDOW:
                        return

                # Add to processed messages
                processed_messages[message_id] = current_time

                logger.info(f"New message from {user}: {text[:50]}...")

                # Add user message to history
                conversation_history.append({"role": "user", "content": text})

                # Generate and send response with history
                reply = generate_response(text, conversation_history)
                logger.info(f"Responding: {reply[:50]}...")

                # Add bot response to history
                conversation_history.append({"role": "assistant", "content": reply})

                # Keep history size manageable
                if len(conversation_history) > AGENT_MAX_HISTORY * 2:
                    conversation_history[:] = conversation_history[-AGENT_MAX_HISTORY:]

                send_message(CHANNEL_ID, reply)
        else:
            # Acknowledge other request types
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)
            
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        # Still acknowledge the request to prevent retries
        try:
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)
        except:
            pass

def main():
    logger.info(f"{AGENT_NAME} is starting...")
    logger.info(f"Using OpenRouter API with model: {AGENT_LLM}")
    logger.info(f"Monitoring channel: {CHANNEL_ID}")

    # Set up event listener
    socket_client.socket_mode_request_listeners.append(process_event)

    # Connect with better error handling
    try:
        logger.info("Connecting to Socket Mode...")
        socket_client.connect()
        logger.info("✓ Socket Mode connected!")
    except Exception as e:
        logger.error(f"Failed to connect to Socket Mode: {e}")
        logger.error("\nTroubleshooting:")
        logger.error("1. Make sure Socket Mode is enabled in your app settings")
        logger.error("2. Make sure Event Subscriptions are enabled")
        logger.error("3. Try regenerating the Socket Mode token")
        return

    logger.info(f"\n{AGENT_NAME} is ready!")
    logger.info("Real-time message processing enabled")
    logger.info("Press Ctrl+C to stop\n")

    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
        socket_client.close()

if __name__ == "__main__":
    main() 