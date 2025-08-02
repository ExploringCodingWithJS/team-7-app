import asyncio
import random
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from anthropic import Anthropic
from models import (
    EmergencyTeam, CrisisResource, CrisisLocation, MessageType, 
    Message, AgentConfig, GameState, EmergencyVocabulary
)
from loguru import logger

class EmergencyTeamAgent:
    def __init__(self, config: AgentConfig, api_key: str):
        self.config = config
        self.client = Anthropic(api_key=api_key)
        self.conversation_history: List[Dict[str, str]] = []
        self.vocabulary: Dict[str, str] = {}
        self.last_response_time = 0
        self.transmission_count = 0

    async def generate_response(self, game_state: GameState, recent_messages: List[Message]) -> Optional[Message]:
        """Generate an emergency response message (8-character limit)"""
        try:
            # Check transmission limits
            team_status = game_state.team_statuses[self.config.team]
            if team_status.transmissions_used >= self.config.max_transmissions:
                return None

            # Check cooldown
            if team_status.last_transmission_time:
                time_since_last = (datetime.now() - team_status.last_transmission_time).total_seconds()
                if time_since_last < self.config.transmission_cooldown:
                    return None

            # Determine if we should respond
            if not self._should_respond(game_state, recent_messages):
                return None

            # Get team perspective
            perspective = self._get_team_perspective(game_state, recent_messages)
            
            # Generate system prompt
            system_prompt = self._create_system_prompt()
            
            # Generate user prompt
            user_prompt = self._create_user_prompt(perspective, recent_messages)
            
            # Call LLM
            response = await self._call_llm(system_prompt, user_prompt)
            
            if response:
                # Extract and validate message
                message_content = self._extract_message_content(response)
                if message_content and len(message_content) <= 8:
                    # Create message
                    message = Message(
                        team=self.config.team,
                        content=message_content,
                        message_type=self._determine_message_type(message_content),
                        timestamp=datetime.now(),
                        is_urgent=self._is_urgent_message(message_content),
                        target_team=self._extract_target_team(message_content, recent_messages),
                        location=self._extract_location(message_content)
                    )
                    
                    # Update vocabulary
                    self._update_vocabulary(message_content, game_state)
                    
                    # Update transmission count
                    team_status.transmissions_used += 1
                    team_status.last_transmission_time = datetime.now()
                    
                    return message
            
            return None
            
        except Exception as e:
            logger.error(f"Error generating response for {self.config.team.value}: {e}")
            return None

    def _should_respond(self, game_state: GameState, recent_messages: List[Message]) -> bool:
        """Determine if the agent should respond based on urgency and situation"""
        team_status = game_state.team_statuses[self.config.team]
        crisis_state = game_state.crisis_state
        
        # Always respond to urgent situations
        if self._is_urgent_situation(crisis_state):
            return True
            
        # Respond to direct requests
        if self._has_direct_request(recent_messages):
            return True
            
        # Respond to resource conflicts
        if self._has_resource_conflict(game_state):
            return True
            
        # Random response based on urgency threshold
        return random.random() < self.config.urgency_threshold

    def _is_urgent_situation(self, crisis_state) -> bool:
        """Check if there's an urgent situation requiring immediate response"""
        return (
            crisis_state.gas_pressure_level >= 7 or
            crisis_state.building_stability <= 3 or
            any(count >= 3 for count in crisis_state.victim_locations.values())
        )

    def _has_direct_request(self, recent_messages: List[Message]) -> bool:
        """Check if there's a direct request to this team"""
        if not recent_messages:
            return False
            
        last_message = recent_messages[-1]
        return (
            last_message.target_team == self.config.team or
            self.config.team.value in last_message.content.upper()
        )

    def _has_resource_conflict(self, game_state: GameState) -> bool:
        """Check if there's a resource conflict involving this team"""
        resources = game_state.resource_allocation
        
        # Check if our resources are being requested
        if self.config.team == EmergencyTeam.FIRE and resources.ladder_owner != self.config.team:
            return True
        if self.config.team == EmergencyTeam.MEDICAL and not resources.ambulance_1_owner:
            return True
            
        return False

    def _get_team_perspective(self, game_state: GameState, recent_messages: List[Message]) -> Dict[str, Any]:
        """Get the current perspective for this team"""
        team_status = game_state.team_statuses[self.config.team]
        crisis_state = game_state.crisis_state
        resources = game_state.resource_allocation
        
        return {
            "team": self.config.team.value,
            "location": team_status.location.value,
            "priority": team_status.priority,
            "transmissions_used": team_status.transmissions_used,
            "max_transmissions": self.config.max_transmissions,
            "time_remaining": game_state.game_duration - crisis_state.time_elapsed,
            
            # Crisis situation
            "fire_locations": [loc.value for loc in crisis_state.fire_locations],
            "victim_locations": {loc.value: count for loc, count in crisis_state.victim_locations.items()},
            "blocked_routes": [loc.value for loc in crisis_state.blocked_routes],
            "gas_pressure": crisis_state.gas_pressure_level,
            "building_stability": crisis_state.building_stability,
            
            # Resource status
            "ladder_location": resources.ladder_location.value if resources.ladder_location else "NONE",
            "ladder_owner": resources.ladder_owner.value if resources.ladder_owner else "NONE",
            "ladder_eta": resources.ladder_eta,
            "ambulance_1_location": resources.ambulance_1_location.value if resources.ambulance_1_location else "NONE",
            "ambulance_2_location": resources.ambulance_2_location.value if resources.ambulance_2_location else "NONE",
            "evac_route_status": resources.evac_route_status,
            
            # Team performance
            "victims_saved": team_status.victims_saved,
            "fire_contained": team_status.fire_contained,
            "people_evacuated": team_status.people_evacuated,
            
            # Recent messages (last 3)
            "recent_messages": [
                {
                    "team": msg.team.value,
                    "content": msg.content,
                    "urgent": msg.is_urgent
                }
                for msg in recent_messages[-3:]
            ]
        }

    def _create_system_prompt(self) -> str:
        """Create the system prompt for the LLM"""
        return f"""You are the {self.config.team.value} TEAM in an emergency response scenario.

CRITICAL RULES:
1. You MUST respond with EXACTLY 8 characters or fewer
2. Use emergency radio protocol - be urgent and direct
3. Focus on your team's priority: {self.config.priority_focus}
4. Coordinate with other teams for shared resources
5. Use shorthand and abbreviations to fit 8 characters

Your team: {self.config.name}
Priority: {self.config.priority_focus}
Available resources: {[r.value for r in self.config.available_resources]}

Examples of 8-character messages:
- "L→SUPR?" (Ladder for suppression?)
- "‼️3V-F4" (URGENT: 3 victims on Floor 4)
- "RTE-RDY" (Route ready)
- "AMB→F4" (Ambulance to Floor 4)
- "F3✓2V" (Floor 3 clear, 2 victims)
- "EVAC-CLR" (Evacuation clear)

Respond with ONLY the 8-character message, nothing else."""

    def _create_user_prompt(self, perspective: Dict[str, Any], recent_messages: List[Message]) -> str:
        """Create the user prompt with current situation"""
        prompt = f"""EMERGENCY SITUATION UPDATE:

Your status: {perspective['team']} at {perspective['location']}
Priority: {perspective['priority']}
Transmissions: {perspective['transmissions_used']}/{perspective['max_transmissions']}
Time remaining: {perspective['time_remaining']}s

CRISIS STATE:
- Fire locations: {perspective['fire_locations']}
- Victims: {perspective['victim_locations']}
- Blocked routes: {perspective['blocked_routes']}
- Gas pressure: {perspective['gas_pressure']}/10
- Building stability: {perspective['building_stability']}/10

RESOURCES:
- Ladder: {perspective['ladder_location']} (owner: {perspective['ladder_owner']})
- Ambulance 1: {perspective['ambulance_1_location']}
- Ambulance 2: {perspective['ambulance_2_location']}
- Evac route: {perspective['evac_route_status']}

YOUR PERFORMANCE:
- Victims saved: {perspective['victims_saved']}
- Fire contained: {perspective['fire_contained']}
- People evacuated: {perspective['people_evacuated']}

RECENT MESSAGES:"""

        for msg in perspective['recent_messages']:
            urgency = "‼️" if msg['urgent'] else ""
            prompt += f"\n- {msg['team']}: {urgency}{msg['content']}"

        prompt += f"""

Based on this situation, send your next 8-character emergency message:"""

        return prompt

    async def _call_llm(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Call the LLM to generate a response"""
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=20,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"LLM call failed for {self.config.team.value}: {e}")
            return None

    def _extract_message_content(self, response: str) -> Optional[str]:
        """Extract the 8-character message from LLM response"""
        if not response:
            return None
            
        # Clean up the response
        content = response.strip().upper()
        
        # Remove quotes if present
        content = content.strip('"\'')
        
        # Take first 8 characters
        if len(content) > 8:
            content = content[:8]
            
        # Ensure it's not empty
        if not content or content.isspace():
            return None
            
        return content

    def _determine_message_type(self, content: str) -> MessageType:
        """Determine the type of message based on content"""
        content_upper = content.upper()
        
        if "?" in content:
            return MessageType.RESOURCE_REQUEST
        elif "‼️" in content or "!" in content:
            return MessageType.URGENT_ALERT
        elif any(word in content_upper for word in ["RTE", "EVAC", "CLEAR", "BLOCK"]):
            return MessageType.COORDINATION
        elif any(word in content_upper for word in ["FIRE", "SUPR", "VICTIM", "AMB"]):
            return MessageType.STATUS_UPDATE
        else:
            return MessageType.STATUS_UPDATE

    def _is_urgent_message(self, content: str) -> bool:
        """Determine if message is urgent"""
        return "‼️" in content or "!" in content or any(word in content.upper() for word in ["URGENT", "EMERGENCY", "HELP"])

    def _extract_target_team(self, content: str, recent_messages: List[Message]) -> Optional[EmergencyTeam]:
        """Extract target team from message content"""
        content_upper = content.upper()
        
        if "FIRE" in content_upper or "L→" in content:
            return EmergencyTeam.FIRE
        elif "MED" in content_upper or "AMB" in content:
            return EmergencyTeam.MEDICAL
        elif "POL" in content_upper or "RTE" in content:
            return EmergencyTeam.POLICE
            
        return None

    def _extract_location(self, content: str) -> Optional[CrisisLocation]:
        """Extract location from message content"""
        content_upper = content.upper()
        
        if "F1" in content_upper:
            return CrisisLocation.FLOOR_1
        elif "F2" in content_upper:
            return CrisisLocation.FLOOR_2
        elif "F3" in content_upper:
            return CrisisLocation.FLOOR_3
        elif "F4" in content_upper:
            return CrisisLocation.FLOOR_4
        elif "EW" in content_upper:
            return CrisisLocation.EAST_WING
        elif "WW" in content_upper:
            return CrisisLocation.WEST_WING
        elif "LB" in content_upper:
            return CrisisLocation.LOBBY
        elif "EXT" in content_upper:
            return CrisisLocation.EXTERIOR
            
        return None

    def _update_vocabulary(self, content: str, game_state: GameState):
        """Update the emergent vocabulary for this team"""
        vocab = game_state.emergency_vocabulary[self.config.team]
        
        # Check for new shorthand
        if len(content) <= 4 and content not in vocab.vocabulary:
            vocab.vocabulary[content] = f"Shorthand for emergency communication"
            vocab.shorthand_developed += 1
            
        # Check for coordination terms
        if any(word in content.upper() for word in ["RTE", "COORD", "SHARE", "HELP"]):
            vocab.coordination_terms += 1
            
        # Check for urgency terms
        if "‼️" in content or "!" in content:
            vocab.urgency_terms += 1 