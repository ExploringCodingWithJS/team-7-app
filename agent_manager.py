import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional
from anthropic import Anthropic
from models import (
    EmergencyTeam, CrisisResource, CrisisLocation, MessageType,
    Message, AgentConfig, GameState, CoordinationEvent
)
from game_engine import CrisisGameEngine
from agent import EmergencyTeamAgent
from slack_integration import SlackIntegration
from loguru import logger

class EmergencyResponseManager:
    def __init__(self, api_key: str, slack_integration: SlackIntegration):
        self.api_key = api_key
        self.slack_integration = slack_integration
        self.game_engine = CrisisGameEngine()
        self.game_state: Optional[GameState] = None
        self.agents: Dict[EmergencyTeam, EmergencyTeamAgent] = {}
        self.running = False
        self.shutdown_event = asyncio.Event()
        
        # Game timing
        self.observation_interval = 5  # Check for responses every 5 seconds
        self.game_duration = 300  # 5 minutes
        self.crisis_update_interval = 120  # Crisis events every 2 minutes

    async def start_game(self):
        """Start the emergency response game"""
        logger.info("🚨 Starting Three-Team Emergency Response Game")
        
        # Initialize game state
        self.game_state = self.game_engine.initialize_game()
        
        # Create agent configurations
        agent_configs = self.game_engine.create_agent_configs()
        
        # Initialize agents
        for team, config in agent_configs.items():
            self.agents[team] = EmergencyTeamAgent(config, self.api_key)
            logger.info(f"✓ {config.name} initialized")
        
        # Send game start message
        await self.slack_integration.send_message(
            f"🚨 **EMERGENCY RESPONSE MISSION STARTED** 🚨\n"
            f"3 emergency teams deployed to apartment building explosion.\n"
            f"**5 minutes to coordinate and save lives!**\n"
            f"Teams: Fire 🔥 | Medical 🚑 | Police 👮\n"
            f"**START COORDINATING!**\n"
            f"DEBUG: Initial conditions - Gas: {self.game_state.crisis_state.gas_pressure_level}, Stability: {self.game_state.crisis_state.building_stability}, Victims: {sum(self.game_state.crisis_state.victim_locations.values())}"
        )
        
        self.running = True
        start_time = datetime.now()
        
        try:
            # Main game loop
            while self.running and not self.shutdown_event.is_set():
                current_time = datetime.now()
                elapsed_time = int((current_time - start_time).total_seconds())
                
                # Check if game is over (time limit or problem solved)
                if elapsed_time >= self.game_duration:
                    await self._end_game("Time limit reached")
                    break
                
                # Check if problem is solved
                if self.game_engine.is_problem_solved(self.game_state):
                    await self._end_game("Problem solved successfully!")
                    break
                
                # Update crisis state
                self.game_engine.update_crisis_state(self.game_state, elapsed_time)
                
                # Check for critical conditions and send immediate alerts
                await self._check_critical_conditions(elapsed_time)
                
                # Process agent responses
                await self._process_agent_round()
                
                # Send crisis updates - more frequent
                if elapsed_time % 30 == 0 and elapsed_time > 0:  # Every 30 seconds
                    await self._send_crisis_update(elapsed_time)
                
                # Send periodic status updates
                if elapsed_time % 45 == 0 and elapsed_time > 0:  # Every 45 seconds
                    await self._send_status_update(elapsed_time)
                
                # Wait before next round
                await asyncio.sleep(self.observation_interval)
                
        except KeyboardInterrupt:
            logger.info("Game interrupted by user")
        except Exception as e:
            logger.error(f"Error in game loop: {e}")
        finally:
            await self._end_game()

    async def _process_agent_round(self):
        """Process one round of agent responses"""
        if not self.game_state:
            return
            
        recent_messages = self.game_state.messages[-10:]  # Last 10 messages
        logger.info(f"🔄 Processing agent round - {len(self.agents)} teams, {len(recent_messages)} recent messages")
        
        # Process each team
        for team, agent in self.agents.items():
            try:
                logger.info(f"🎯 Processing {team.value} team...")
                # Generate response
                message = await agent.generate_response(self.game_state, recent_messages)
                
                if message:
                    logger.info(f"✅ {team.value} generated message: {message.content}")
                    # Add message to game state
                    self.game_state.messages.append(message)
                    
                    # Send to Slack
                    await self._send_agent_message(message)
                    
                    # Check for coordination events
                    await self._check_coordination_events(message)
                    
                    # Add random delay (radio interference simulation)
                    await asyncio.sleep(random.uniform(0.1, 0.3))
                else:
                    logger.info(f"❌ {team.value} generated no message")
                    
            except Exception as e:
                logger.error(f"Error processing {team.value} agent: {e}")

    async def _send_agent_message(self, message: Message):
        """Send an agent message to Slack"""
        urgency_icon = "‼️" if message.is_urgent else ""
        team_icon = {
            EmergencyTeam.FIRE: "🔥",
            EmergencyTeam.MEDICAL: "🚑", 
            EmergencyTeam.POLICE: "👮"
        }.get(message.team, "🤖")
        
        await self.slack_integration.send_message(
            f"{team_icon} **{message.team.value}**: {urgency_icon}`{message.content}`"
        )

    async def _send_crisis_update(self, elapsed_time: int):
        """Send a crisis update to Slack"""
        if not self.game_state:
            return
            
        crisis_state = self.game_state.crisis_state
        
        # Get random crisis event
        crisis_events = [
            "🚨FLASH#1: Fire spreading to east wing",
            "🚨FLASH#2: Victim found on floor 3", 
            "🚨FLASH#3: Gas pressure building",
            "🚨FLASH#4: Structure collapse on floor 2",
            "🚨FLASH#5: Ambulance arrival delayed",
            "🚨FLASH#6: Evac route blocked by debris"
        ]
        
        event = random.choice(crisis_events)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        
        # Add urgency indicators based on crisis state
        urgency_indicators = []
        if crisis_state.gas_pressure_level >= 7:
            urgency_indicators.append("⚠️ GAS CRITICAL")
        if crisis_state.building_stability <= 3:
            urgency_indicators.append("⚠️ BUILDING UNSTABLE")
        if len(crisis_state.fire_locations) >= 3:
            urgency_indicators.append("⚠️ MULTIPLE FIRES")
        if any(count >= 2 for count in crisis_state.victim_locations.values()):
            urgency_indicators.append("⚠️ VICTIMS TRAPPED")
            
        urgency_text = " | ".join(urgency_indicators) if urgency_indicators else ""
        
        await self.slack_integration.send_message(
            f"🚨 **CRISIS UPDATE** 🚨\n"
            f"{event}\n"
            f"Time: {minutes}:{seconds:02d} | "
            f"Gas: {crisis_state.gas_pressure_level}/10 | "
            f"Building: {crisis_state.building_stability}/10\n"
            f"{urgency_text}"
        )

    async def _send_status_update(self, elapsed_time: int):
        """Send a status update to Slack"""
        if not self.game_state:
            return
            
        team_statuses = self.game_state.team_statuses
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        
        # Calculate totals
        total_victims_saved = sum(team.victims_saved for team in team_statuses.values())
        total_fire_contained = sum(team.fire_contained for team in team_statuses.values())
        total_evacuated = sum(team.people_evacuated for team in team_statuses.values())
        
        await self.slack_integration.send_message(
            f"📊 **STATUS UPDATE** 📊\n"
            f"Time: {minutes}:{seconds:02d} remaining\n"
            f"🔥 Fire: {total_fire_contained} contained | "
            f"🚑 Victims: {total_victims_saved} saved | "
            f"👮 Evacuated: {total_evacuated}\n"
            f"Coordination events: {len(self.game_state.coordination_events)}"
        )

    async def _check_coordination_events(self, message: Message):
        """Check if a message triggers a coordination event"""
        if not self.game_state:
            return
            
        # Check for resource requests
        if message.message_type == MessageType.RESOURCE_REQUEST:
            await self._process_resource_request(message)
            
        # Check for coordination success
        if message.message_type == MessageType.COORDINATION:
            await self._record_coordination_success(message)

    async def _process_resource_request(self, message: Message):
        """Process a resource request between teams"""
        if not self.game_state:
            return
            
        # Extract resource and location from message
        content = message.content.upper()
        
        if "L→" in content or "LADDER" in content:
            # Ladder request
            resource = CrisisResource.LADDER
            location = self._extract_location_from_message(content)
            
            if location:
                success = self.game_engine.process_resource_request(
                    self.game_state, message.team, resource, location
                )
                
                if success:
                    await self.slack_integration.send_message(
                        f"✅ **RESOURCE GRANTED**: {message.team.value} gets ladder at {location.value}"
                    )
                    
                    # Record coordination event
                    self.game_engine.record_coordination_event(
                        self.game_state,
                        "RESOURCE_SHARING",
                        [message.team],
                        resource,
                        location,
                        "SUCCESS"
                    )
                else:
                    await self.slack_integration.send_message(
                        f"❌ **RESOURCE CONFLICT**: Ladder already in use"
                    )
                    
        elif "AMB" in content:
            # Ambulance request
            ambulance_num = 1 if "1" in content else 2
            resource = CrisisResource.AMBULANCE_1 if ambulance_num == 1 else CrisisResource.AMBULANCE_2
            location = self._extract_location_from_message(content)
            
            if location:
                success = self.game_engine.process_resource_request(
                    self.game_state, message.team, resource, location
                )
                
                if success:
                    await self.slack_integration.send_message(
                        f"✅ **AMBULANCE {ambulance_num}**: {message.team.value} gets ambulance at {location.value}"
                    )
                else:
                    await self.slack_integration.send_message(
                        f"❌ **AMBULANCE {ambulance_num}**: Already in use"
                    )

    def _extract_location_from_message(self, content: str) -> Optional[CrisisLocation]:
        """Extract location from message content"""
        if "F1" in content:
            return CrisisLocation.FLOOR_1
        elif "F2" in content:
            return CrisisLocation.FLOOR_2
        elif "F3" in content:
            return CrisisLocation.FLOOR_3
        elif "F4" in content:
            return CrisisLocation.FLOOR_4
        elif "EW" in content:
            return CrisisLocation.EAST_WING
        elif "WW" in content:
            return CrisisLocation.WEST_WING
        elif "LB" in content:
            return CrisisLocation.LOBBY
        elif "EXT" in content:
            return CrisisLocation.EXTERIOR
        return None

    async def _record_coordination_success(self, message: Message):
        """Record a successful coordination event"""
        if not self.game_state:
            return
            
        # Find other teams involved
        other_teams = [team for team in EmergencyTeam if team != message.team]
        
        self.game_engine.record_coordination_event(
            self.game_state,
            "COORDINATION_SUCCESS",
            [message.team] + other_teams,
            outcome="SUCCESS",
            lives_saved=1,
            time_saved=30
        )

    async def _end_game(self, reason: str = "Game ended"):
        """End the game and show results"""
        if not self.game_state:
            return
            
        self.running = False
        
        # Calculate final results
        game_result = self.game_engine.get_game_result(self.game_state)
        
        # Send final summary
        await self.slack_integration.send_message(
            f"🏁 **EMERGENCY RESPONSE MISSION COMPLETE** 🏁\n"
            f"📋 Reason: {reason}\n"
            f"⏱️ Duration: {game_result['duration']}s | "
            f"🏆 Score: {game_result['final_score']:.1f}\n"
            f"🚑 Lives saved: {game_result['lives_saved']} | "
            f"🔥 Fire contained: {game_result['fire_contained']} | "
            f"👮 Evacuated: {game_result['people_evacuated']}\n"
            f"🤝 Coordination events: {game_result['coordination_events']}\n"
            f"📚 Emergent vocabulary: {sum(game_result['emergent_vocabulary'].values())} terms"
        )
        
        # Send team performance
        for team_name, performance in game_result['team_performance'].items():
            await self.slack_integration.send_message(
                f"📊 **{team_name}**: "
                f"Victims: {performance['victims_saved']} | "
                f"Fire: {performance['fire_contained']} | "
                f"Evacuated: {performance['people_evacuated']} | "
                f"Transmissions: {performance['transmissions_used']}"
            )
        
        # Send emergent communication analysis
        await self._send_emergent_communication_summary()
        
        # Export game data
        filename = self.game_engine.export_game_data(self.game_state, game_result)
        logger.info(f"Game data exported to {filename}")
        
        logger.info("Emergency response game completed")

    async def _check_critical_conditions(self, elapsed_time: int):
        """Check for critical conditions and send immediate alerts"""
        if not self.game_state:
            return
            
        crisis_state = self.game_state.crisis_state
        
        # Check for critical gas pressure
        if crisis_state.gas_pressure_level >= 8:
            await self.slack_integration.send_message(
                f"🚨 **CRITICAL ALERT** 🚨\n"
                f"⚠️ GAS PRESSURE CRITICAL: {crisis_state.gas_pressure_level}/10\n"
                f"Building at risk of explosion! Teams must act immediately!"
            )
            
        # Check for critical building stability
        if crisis_state.building_stability <= 2:
            await self.slack_integration.send_message(
                f"🚨 **CRITICAL ALERT** 🚨\n"
                f"⚠️ BUILDING STABILITY CRITICAL: {crisis_state.building_stability}/10\n"
                f"Structure may collapse! Evacuate immediately!"
            )
            
        # Check for multiple victims
        total_victims = sum(crisis_state.victim_locations.values())
        if total_victims >= 4:
            await self.slack_integration.send_message(
                f"🚨 **CRITICAL ALERT** 🚨\n"
                f"⚠️ MULTIPLE VICTIMS: {total_victims} people trapped\n"
                f"Medical team needs immediate assistance!"
            )

    async def _send_emergent_communication_summary(self):
        """Send detailed analysis of emergent communication patterns"""
        if not self.game_state:
            return
            
        # Analyze message patterns
        messages = self.game_state.messages
        total_messages = len(messages)
        
        if total_messages == 0:
            await self.slack_integration.send_message("📊 **No messages recorded**")
            return
        
        # Message type analysis
        message_types = {}
        urgency_count = 0
        resource_requests = 0
        coordination_messages = 0
        
        for msg in messages:
            msg_type = msg.message_type.value
            message_types[msg_type] = message_types.get(msg_type, 0) + 1
            
            if msg.is_urgent:
                urgency_count += 1
            if msg.message_type.value == "resource_request":
                resource_requests += 1
            if msg.message_type.value == "coordination":
                coordination_messages += 1
        
        # Team communication analysis
        team_messages = {}
        for msg in messages:
            team = msg.team.value
            team_messages[team] = team_messages.get(team, 0) + 1
        
        # Vocabulary analysis
        vocab_summary = {}
        for team, vocab in self.game_state.emergency_vocabulary.items():
            vocab_summary[team.value] = {
                "shorthand_terms": vocab.shorthand_developed,
                "coordination_terms": vocab.coordination_terms,
                "urgency_terms": vocab.urgency_terms,
                "total_vocabulary": len(vocab.vocabulary)
            }
        
        # Send detailed summary
        await self.slack_integration.send_message(
            f"📊 **EMERGENT COMMUNICATION ANALYSIS** 📊\n"
            f"📝 Total Messages: {total_messages}\n"
            f"🚨 Urgent Messages: {urgency_count} ({urgency_count/total_messages*100:.1f}%)\n"
            f"🔧 Resource Requests: {resource_requests}\n"
            f"🤝 Coordination Messages: {coordination_messages}"
        )
        
        # Message type breakdown
        type_breakdown = "\n".join([f"• {k.replace('_', ' ').title()}: {v}" for k, v in message_types.items()])
        await self.slack_integration.send_message(
            f"📋 **Message Types:**\n{type_breakdown}"
        )
        
        # Team communication breakdown
        team_breakdown = "\n".join([f"• {team}: {count} messages" for team, count in team_messages.items()])
        await self.slack_integration.send_message(
            f"👥 **Team Communication:**\n{team_breakdown}"
        )
        
        # Vocabulary development
        vocab_breakdown = ""
        for team, stats in vocab_summary.items():
            vocab_breakdown += f"• {team}: {stats['total_vocabulary']} terms "
            vocab_breakdown += f"({stats['shorthand_terms']} shorthand, "
            vocab_breakdown += f"{stats['coordination_terms']} coordination, "
            vocab_breakdown += f"{stats['urgency_terms']} urgency)\n"
        
        await self.slack_integration.send_message(
            f"📚 **Emergent Vocabulary Development:**\n{vocab_breakdown}"
        )
        
        # Sample messages from each team
        await self.slack_integration.send_message("💬 **Sample Messages by Team:**")
        for team in EmergencyTeam:
            team_msgs = [msg for msg in messages if msg.team == team]
            if team_msgs:
                sample_msgs = [msg.content for msg in team_msgs[-3:]]  # Last 3 messages
                sample_text = " | ".join(sample_msgs)
                await self.slack_integration.send_message(f"• {team.value}: {sample_text}")
        
        # Coordination success rate
        coordination_events = self.game_state.coordination_events
        successful_coordinations = len([e for e in coordination_events if e.outcome == "SUCCESS"])
        total_coordinations = len(coordination_events)
        
        if total_coordinations > 0:
            success_rate = successful_coordinations / total_coordinations * 100
            await self.slack_integration.send_message(
                f"✅ **Coordination Success Rate: {success_rate:.1f}%** "
                f"({successful_coordinations}/{total_coordinations})"
            )

    async def handle_game_command(self, command: str):
        """Handle game commands from Slack"""
        if command.upper() == "START_GAME":
            if not self.running:
                await self.start_game()
            else:
                await self.slack_integration.send_message("Game already running!")
        elif command.upper() == "STATUS":
            if self.game_state:
                elapsed_time = int((datetime.now() - self.game_state.start_time).total_seconds())
                await self._send_status_update(elapsed_time)
        elif command.upper() == "STOP":
            self.running = False
            await self.slack_integration.send_message("Game stopped by user")
        elif command.upper() == "QUIT_GAME":
            if self.running:
                await self._end_game("User requested game termination")
            else:
                await self.slack_integration.send_message("No game currently running")
        else:
            await self.slack_integration.send_message(f"Unknown command: {command}")

    async def shutdown(self):
        """Shutdown the game manager"""
        logger.info("Shutting down Emergency Response Manager...")
        self.running = False
        self.shutdown_event.set() 