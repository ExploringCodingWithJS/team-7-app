import asyncio
import json
from typing import List, Dict, Optional, Callable
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.models.blocks import SectionBlock, DividerBlock, ContextBlock
from slack_sdk.models.views import View
from models import Message, AgentConfig
from loguru import logger
import re

class SlackIntegration:
    def __init__(self, bot_token: str, app_token: str, channel_id: str):
        self.bot_token = bot_token
        self.app_token = app_token
        self.channel_id = channel_id
        self.web_client = AsyncWebClient(token=bot_token)
        self.socket_client = SocketModeClient(app_token=app_token, web_client=self.web_client)
        self.message_handlers: List[Callable] = []
        self.agent_messages: List[Message] = []
        self.is_running = False
        
    async def start(self):
        """Start the Slack integration."""
        logger.info("Starting Slack integration...")
        
        # Set up event handlers
        self.socket_client.socket_mode_request_listeners.append(self._handle_socket_request)
        
        # Start the socket client
        await self.socket_client.connect()
        self.is_running = True
        
        logger.info("Slack integration started successfully")
    
    async def stop(self):
        """Stop the Slack integration."""
        logger.info("Stopping Slack integration...")
        self.is_running = False
        await self.socket_client.close()
        logger.info("Slack integration stopped")
    
    async def _handle_socket_request(self, client, req):
        """Handle incoming socket mode requests."""
        if req.type == "events_api":
            await self._handle_event(req.payload)
        
        # Always acknowledge the request
        from slack_sdk.socket_mode.response import SocketModeResponse
        await client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))
    
    async def _handle_event(self, payload):
        """Handle Slack events."""
        event = payload.get("event", {})
        event_type = event.get("type")
        
        if event_type == "message":
            await self._handle_message(event)
        elif event_type == "app_mention":
            await self._handle_app_mention(event)
    
    async def _handle_message(self, event):
        """Handle incoming messages."""
        # Ignore bot messages to prevent loops
        if event.get("bot_id"):
            logger.debug(f"Ignoring bot message: {event.get('bot_id')}")
            return
        
        # Only process messages in our target channel
        if event.get("channel") != self.channel_id:
            logger.debug(f"Ignoring message from different channel: {event.get('channel')} != {self.channel_id}")
            return
        
        message_text = event.get("text", "")
        user_id = event.get("user", "")
        timestamp = event.get("ts", "")
        
        logger.info(f"🔍 DEBUG: Received message from {user_id}: {message_text}")
        
        # Check for START_GAME trigger (handle HTML encoding)
        clean_text = message_text.strip()
        if clean_text == "<START_GAME>" or clean_text == "&lt;START_GAME&gt;":
            logger.info("🎮 START_GAME trigger detected!")
            await self._send_message("🎮 Starting multi-agent coordination game...")
            # Trigger game start
            for handler in self.message_handlers:
                logger.info(f"Calling handler: {handler}")
                await handler("START_GAME")
            return
        
        # Check for START_GAME message (alternative format)
        clean_text = message_text.strip().upper()
        if clean_text == "<START_GAME>" or clean_text == "&LT;START_GAME&GT;":
            await self._send_message("🎮 Starting multi-agent coordination game...")
            # Trigger game start
            for handler in self.message_handlers:
                await handler("START_GAME")
            return
        
        # Check if this is a command for the agents
        if message_text.startswith("/agent"):
            await self._handle_agent_command(message_text, user_id)
        else:
            # Regular message - could be human interaction
            await self._handle_human_message(message_text, user_id, timestamp)
    
    async def _handle_app_mention(self, event):
        """Handle app mentions."""
        message_text = event.get("text", "")
        user_id = event.get("user", "")
        
        # Remove the bot mention
        clean_text = re.sub(r'<@[A-Z0-9]+>', '', message_text).strip()
        
        await self._handle_agent_command(clean_text, user_id)
    
    async def _handle_agent_command(self, command: str, user_id: str):
        """Handle commands directed at agents."""
        # Parse command
        parts = command.split()
        if len(parts) < 2:
            await self._send_message("Please specify a command. Available commands: start, stop, status, help")
            return
        
        cmd = parts[1].lower()
        
        if cmd == "start":
            await self._send_message("Starting multi-agent coordination game...")
            # Trigger game start
            for handler in self.message_handlers:
                await handler("START_GAME")
        
        elif cmd == "stop":
            await self._send_message("Stopping multi-agent coordination game...")
            # Trigger game stop
            for handler in self.message_handlers:
                await handler("STOP")
        
        elif cmd == "status":
            await self._send_status_message()
        
        elif cmd == "help":
            await self._send_help_message()
        
        else:
            await self._send_message(f"Unknown command: {cmd}. Use 'help' for available commands.")
    
    async def _handle_human_message(self, message_text: str, user_id: str, timestamp: str):
        """Handle messages from human users."""
        # For now, just log human messages
        logger.info(f"Human message: {message_text}")
        
        # Could be used for human-in-the-loop scenarios
        # For now, we'll just acknowledge
        await self._send_message(f"Human input received: {message_text[:50]}...")
    
    async def send_agent_message(self, agent_config: AgentConfig, content: str, message_type: str = "observation"):
        """Send a message from an agent to the Slack channel."""
        try:
            # Send simple text message instead of blocks to avoid formatting issues
            response = await self.web_client.chat_postMessage(
                channel=self.channel_id,
                text=f"*{agent_config.name}* ({agent_config.role.value.replace('_', ' ').title()}):\n{content}"
            )
            
            if response["ok"]:
                # Create and store message object
                message = Message(
                    agent_id=agent_config.agent_id,
                    content=content,
                    message_type=message_type
                )
                self.agent_messages.append(message)
                
                logger.info(f"Agent {agent_config.name} message sent successfully")
                return message
            else:
                logger.error(f"Failed to send agent message: {response.get('error')}")
                return None
                
        except Exception as e:
            logger.error(f"Error sending agent message: {e}")
            return None
    
    async def send_game_status(self, game_state: Dict, score: float):
        """Send game status update."""
        try:
            # Create status text for maze game
            explored_cells = sum(1 for cell in game_state.get("cells", []) if cell.get("is_explored", False))
            total_cells = len(game_state.get("cells", []))
            agents_at_exit = len(game_state.get("agents_at_exit", []))
            total_agents = len(game_state.get("agent_positions", {}))
            
            status_text = f"""*Maze Exploration Status*
Phase: {game_state.get('phase', 'unknown')}
Round: {game_state.get('round_number', 0)}
Score: {score:.2f}

*Exploration Progress:*
• Explored: {explored_cells}/{total_cells} cells ({explored_cells/total_cells*100:.1f}%)
• Exit Found: {'✅' if game_state.get('exit_found', False) else '❌'}
• Agents at Exit: {agents_at_exit}/{total_agents}
• Time Remaining: {game_state.get('time_remaining', 300)}s"""
            
            await self.web_client.chat_postMessage(
                channel=self.channel_id,
                text=status_text
            )
            
        except Exception as e:
            logger.error(f"Error sending game status: {e}")
    
    async def send_coordination_event(self, event: Dict):
        """Send coordination event notification."""
        try:
            event_type = event.get("event_type", "unknown")
            description = event.get("description", "")
            participants = event.get("participants", [])
            
            event_text = f"""*Coordination Event: {event_type.replace('_', ' ').title()}*
{description}

*Details:*
• Participants: {len(participants)} agents
• Event ID: {event.get('event_id', 'unknown')[:8]}"""
            
            await self.web_client.chat_postMessage(
                channel=self.channel_id,
                text=event_text
            )
            
        except Exception as e:
            logger.error(f"Error sending coordination event: {e}")
    
    async def send_analysis_report(self, analysis_data: Dict):
        """Send analysis report of emergent behaviors."""
        try:
            vocabulary = analysis_data.get("emergent_vocabulary", {})
            patterns = analysis_data.get("communication_patterns", [])
            metrics = analysis_data.get("efficiency_metrics", {})
            
            # Format vocabulary
            vocab_text = ""
            for term, data in list(vocabulary.items())[:5]:  # Show top 5
                usage_count = data.get("usage_count", 0)
                vocab_text += f"• {term}: {usage_count} uses\n"
            
            # Format patterns
            patterns_text = ""
            for pattern in patterns[:3]:  # Show top 3
                patterns_text += f"• {pattern[:50]}...\n"
            
            # Send simple text instead of blocks
            report_text = f"""*Emergent Communication Analysis*

*Emergent Vocabulary:*
{vocab_text}

*Communication Patterns:*
{patterns_text}

*Metrics:*
• Total Events: {metrics.get('total_coordination_events', 0)}
• Success Rate: {metrics.get('successful_coordinations', 0)}/{metrics.get('total_coordination_events', 1)}"""
            
            await self.web_client.chat_postMessage(
                channel=self.channel_id,
                text=report_text
            )
            
        except Exception as e:
            logger.error(f"Error sending analysis report: {e}")
    
    async def _send_message(self, text: str):
        """Send a simple text message."""
        try:
            await self.web_client.chat_postMessage(
                channel=self.channel_id,
                text=text
            )
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def send_message(self, text: str):
        """Send a simple text message (public method)."""
        await self._send_message(text)
    
    async def _send_status_message(self):
        """Send current game status."""
        status_text = """
*Multi-Agent Coordination Game Status*

🟢 System: Running
🎮 Game: Active
🤖 Agents: 4 active
📊 Phase: Discovery
📈 Score: Calculating...

Use `/agent help` for available commands.
"""
        await self._send_message(status_text)
    
    async def _send_help_message(self):
        """Send help message with available commands."""
        help_text = """
*Multi-Agent Coordination Game Commands*

`<START_GAME>` - Start a new coordination game (simple trigger)
`/agent start` - Start a new coordination game
`/agent stop` - Stop the current game
`/agent status` - Show current game status
`/agent help` - Show this help message

*About the Game:*
This is a research system studying emergent communication patterns in multi-agent coordination. Agents develop their own language and strategies to solve resource allocation challenges.
"""
        await self._send_message(help_text)
    
    def add_message_handler(self, handler: Callable):
        """Add a message handler for game events."""
        self.message_handlers.append(handler)
    
    def get_recent_messages(self, limit: int = 20) -> List[Message]:
        """Get recent agent messages."""
        return self.agent_messages[-limit:] if self.agent_messages else []
    
    def clear_messages(self):
        """Clear stored messages."""
        self.agent_messages.clear() 