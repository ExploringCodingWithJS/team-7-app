#!/usr/bin/env python3
"""
Multi-Agent Coordination Game: Resource Allocation Puzzle

This system studies emergent communication patterns in multi-agent coordination.
Agents develop their own language and strategies to solve resource allocation challenges.
"""

import asyncio
import os
from dotenv import load_dotenv
from loguru import logger
from slack_integration import SlackIntegration
from agent_manager import EmergencyResponseManager

def setup_logging():
    """Set up logging configuration"""
    logger.remove()  # Remove default handler
    logger.add(
        lambda msg: print(msg, end=""),
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )

def create_directories():
    """Create necessary directories"""
    os.makedirs("logs", exist_ok=True)

async def main():
    """Main entry point for the Emergency Response Game"""
    setup_logging()
    create_directories()
    
    # Load environment variables
    load_dotenv()
    
    # Get required environment variables
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
    slack_app_token = os.getenv("SLACK_APP_TOKEN")
    slack_channel_id = os.getenv("SLACK_CHANNEL_ID")
    
    # Validate environment variables
    missing_vars = []
    if not anthropic_api_key:
        missing_vars.append("ANTHROPIC_API_KEY")
    if not slack_bot_token:
        missing_vars.append("SLACK_BOT_TOKEN")
    if not slack_app_token:
        missing_vars.append("SLACK_APP_TOKEN")
    if not slack_channel_id:
        missing_vars.append("SLACK_CHANNEL_ID")
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please check your .env file")
        return
    
    logger.info("🚨 Emergency Response Game System Starting...")
    logger.info("Using Anthropic Claude for agent intelligence")
    logger.info(f"Slack Channel: {slack_channel_id}")
    
    try:
        # Initialize Slack integration
        slack_integration = SlackIntegration(slack_bot_token, slack_app_token, slack_channel_id)
        
        # Initialize emergency response manager
        manager = EmergencyResponseManager(anthropic_api_key, slack_integration)
        
        # Set up message handler
        slack_integration.add_message_handler(manager.handle_game_command)
        
        # Start Slack integration
        await slack_integration.start()
        
        # Send welcome message
        await slack_integration.send_message(
            "🚨 **Emergency Response Coordination System** 🚨\n\n"
            "Three emergency teams (Fire 🔥, Medical 🚑, Police 👮) must coordinate "
            "during a crisis scenario.\n\n"
            "**Features:**\n"
            "• 8-character emergency radio protocol\n"
            "• Resource negotiation (ladder, ambulances)\n"
            "• Dynamic crisis events every 2 minutes\n"
            "• 5-minute time limit\n"
            "• Emergent communication patterns\n\n"
            "Type `<START_GAME>` to begin the emergency response mission!"
        )
        
        logger.info("✅ System ready! Type <START_GAME> in Slack to begin")
        logger.info("Press Ctrl+C to stop")
        
        # Keep running until interrupted
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n🛑 Shutting down...")
            await manager.shutdown()
            await slack_integration.stop()
            
    except Exception as e:
        logger.error(f"Error starting system: {e}")
        return

if __name__ == "__main__":
    asyncio.run(main()) 