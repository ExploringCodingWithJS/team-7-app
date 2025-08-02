import os
import time
import asyncio
import requests
from slack_sdk import WebClient
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from datetime import datetime
from dotenv import load_dotenv
import logging
from collections import deque
from threading import Lock

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Agent Configuration
AGENT_NAME = "Rate-Limited Slack AI Agent"
AGENT_LLM = "openai/gpt-4"
AGENT_LLM_SYSTEM_PROMPT = "You are a helpful assistant agent in a Slack channel."
AGENT_LLM_TEMPERATURE = 0.7
AGENT_LLM_MAX_TOKENS = 1000
AGENT_MAX_HISTORY = 10

# Load configuration from environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Rate Limiting Configuration
SLACK_RATE_LIMIT = 1.0  # 1 request per second (free tier)
MESSAGE_QUEUE_SIZE = 100
MAX_CONCURRENT_REQUESTS = 3

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

# Rate Limiting State
message_queue = deque(maxlen=MESSAGE_QUEUE_SIZE)
last_message_time = 0
queue_lock = Lock()
active_requests = 0
request_lock = Lock()

# Store recent conversation history
conversation_history = []

# Track processed messages with cleanup
processed_messages = {}
MESSAGE_DEDUP_WINDOW = 30  # seconds
MAX_PROCESSED_MESSAGES = 1000

class RateLimitedSlackAgent:
    def __init__(self):
        self.socket_client = None
        self.running = False
        
    async def cleanup_old_messages(self):
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

    async def generate_response(self, prompt, history=None):
        """Generate response using OpenRouter API with retry logic"""
        global active_requests
        
        # Check concurrent request limit
        with request_lock:
            if active_requests >= MAX_CONCURRENT_REQUESTS:
                logger.warning("Too many concurrent requests, skipping")
                return "I'm a bit busy right now. Please try again in a moment."
            active_requests += 1
        
        try:
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
                        await asyncio.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    else:
                        return "Sorry, there was an error generating a response."
                except Exception as e:
                    logger.error(f"Unexpected error generating response: {e}")
                    return "Sorry, there was an error generating a response."
        finally:
            with request_lock:
                active_requests -= 1

    async def send_message_with_rate_limit(self, channel, text):
        """Send a message to Slack with rate limiting"""
        global last_message_time
        
        # Calculate time since last message
        current_time = time.time()
        time_since_last = current_time - last_message_time
        
        # If we need to wait, add to queue
        if time_since_last < SLACK_RATE_LIMIT:
            wait_time = SLACK_RATE_LIMIT - time_since_last
            logger.info(f"Rate limited. Waiting {wait_time:.2f} seconds...")
            await asyncio.sleep(wait_time)
        
        try:
            response = web_client.chat_postMessage(
                channel=channel,
                text=text
            )
            last_message_time = time.time()
            logger.info(f"Message sent successfully (rate limited)")
            return response
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            # If rate limited, wait and retry once
            if "ratelimited" in str(e).lower():
                logger.info("Slack rate limit hit, waiting 2 seconds...")
                await asyncio.sleep(2)
                try:
                    response = web_client.chat_postMessage(
                        channel=channel,
                        text=text
                    )
                    last_message_time = time.time()
                    logger.info(f"Message sent successfully (retry)")
                    return response
                except Exception as e2:
                    logger.error(f"Retry failed: {e2}")
            return None

    async def process_event(self, client: SocketModeClient, req: SocketModeRequest):
        """Process incoming events with rate limiting"""
        try:
            if req.type == "events_api":
                # Acknowledge the request immediately
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
                        await self.cleanup_old_messages()

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

                    # Generate response (this is async and can take time)
                    reply = await self.generate_response(text, conversation_history)
                    logger.info(f"Generated response: {reply[:50]}...")

                    # Add bot response to history
                    conversation_history.append({"role": "assistant", "content": reply})

                    # Keep history size manageable
                    if len(conversation_history) > AGENT_MAX_HISTORY * 2:
                        conversation_history[:] = conversation_history[-AGENT_MAX_HISTORY:]

                    # Send message with rate limiting
                    await self.send_message_with_rate_limit(CHANNEL_ID, reply)
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

    async def start(self):
        """Start the rate-limited Slack agent"""
        logger.info(f"{AGENT_NAME} is starting...")
        logger.info(f"Using OpenRouter API with model: {AGENT_LLM}")
        logger.info(f"Monitoring channel: {CHANNEL_ID}")
        logger.info(f"Rate limit: {SLACK_RATE_LIMIT} requests per second")

        # Initialize socket client
        self.socket_client = SocketModeClient(
            app_token=SLACK_APP_TOKEN,
            web_client=web_client
        )

        # Set up event listener
        self.socket_client.socket_mode_request_listeners.append(self.process_event)

        # Connect with better error handling
        try:
            logger.info("Connecting to Socket Mode...")
            await self.socket_client.connect()
            logger.info("✓ Socket Mode connected!")
        except Exception as e:
            logger.error(f"Failed to connect to Socket Mode: {e}")
            logger.error("\nTroubleshooting:")
            logger.error("1. Make sure Socket Mode is enabled in your app settings")
            logger.error("2. Make sure Event Subscriptions are enabled")
            logger.error("3. Try regenerating the Socket Mode token")
            return

        self.running = True
        logger.info(f"\n{AGENT_NAME} is ready!")
        logger.info("Real-time message processing with rate limiting enabled")
        logger.info("Press Ctrl+C to stop\n")

        try:
            # Keep running
            while self.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("\nShutting down...")
            self.running = False
            await self.socket_client.close()

async def main():
    agent = RateLimitedSlackAgent()
    await agent.start()

if __name__ == "__main__":
    asyncio.run(main()) 