import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from models import (
    EmergencyTeam, CrisisResource, CrisisLocation, CrisisEvent, 
    CrisisState, ResourceAllocation, TeamStatus, GameState, 
    AgentConfig, CoordinationEvent, EmergencyVocabulary
)

class CrisisGameEngine:
    def __init__(self):
        self.crisis_scenarios = [
            "🚨FLASH#1: Fire spreading to east wing",
            "🚨FLASH#2: Victim found on floor 3",
            "🚨FLASH#3: Gas pressure building",
            "🚨FLASH#4: Structure collapse on floor 2",
            "🚨FLASH#5: Ambulance arrival delayed",
            "🚨FLASH#6: Evac route blocked by debris"
        ]
        self.crisis_timer = 0
        self.next_crisis_time = 15  # 15 seconds (was 120)

    def initialize_game(self) -> GameState:
        """Initialize the emergency response game"""
        game_id = str(uuid.uuid4())
        
        # Initialize crisis state
        crisis_state = CrisisState(
            fire_locations=[CrisisLocation.FLOOR_2, CrisisLocation.EAST_WING],
            victim_locations={
                CrisisLocation.FLOOR_3: 2,
                CrisisLocation.FLOOR_4: 1,
                CrisisLocation.LOBBY: 3
            },
            blocked_routes=[CrisisLocation.FLOOR_1],
            gas_pressure_level=3,
            building_stability=7,
            time_elapsed=0
        )
        
        # Initialize resource allocation
        resource_allocation = ResourceAllocation(
            ladder_location=CrisisLocation.EXTERIOR,
            ladder_owner=None,
            evac_route_status="BLOCKED",
            evac_route_controller=None
        )
        
        # Initialize team statuses
        team_statuses = {
            EmergencyTeam.FIRE: TeamStatus(
                team=EmergencyTeam.FIRE,
                location=CrisisLocation.EXTERIOR,
                resources_available=[CrisisResource.LADDER, CrisisResource.WATER_SUPPLY],
                priority="FIRE_SUPPRESSION"
            ),
            EmergencyTeam.MEDICAL: TeamStatus(
                team=EmergencyTeam.MEDICAL,
                location=CrisisLocation.LOBBY,
                resources_available=[CrisisResource.MEDICAL_SUPPLIES],
                priority="VICTIM_RESCUE"
            ),
            EmergencyTeam.POLICE: TeamStatus(
                team=EmergencyTeam.POLICE,
                location=CrisisLocation.EXTERIOR,
                resources_available=[],
                priority="EVACUATION_CONTROL"
            )
        }
        
        # Initialize emergency vocabulary for each team
        emergency_vocabulary = {
            team: EmergencyVocabulary(team=team)
            for team in EmergencyTeam
        }
        
        return GameState(
            game_id=game_id,
            start_time=datetime.now(),
            crisis_state=crisis_state,
            resource_allocation=resource_allocation,
            team_statuses=team_statuses,
            emergency_vocabulary=emergency_vocabulary
        )

    def create_agent_configs(self) -> Dict[EmergencyTeam, AgentConfig]:
        """Create configurations for each emergency team"""
        configs = {}
        
        # Fire Team Configuration
        configs[EmergencyTeam.FIRE] = AgentConfig(
            team=EmergencyTeam.FIRE,
            name="Fire Team Alpha",
            system_prompt="""You are the FIRE TEAM in an emergency response scenario. Your priorities are:
1. FIRE SUPPRESSION - Control and extinguish fires
2. RESCUE OPERATIONS - Use ladder for victim rescue
3. STRUCTURE ASSESSMENT - Evaluate building stability

You have the LADDER resource. You must negotiate with other teams for:
- Medical team needs ladder for victim access
- Police team needs clear routes for evacuation

Use 8-character messages maximum. Be urgent and direct.
Examples: "L→SUPR?" (Ladder for suppression?), "F3✓2V" (Floor 3 clear, 2 victims)""",
            priority_focus="FIRE_SUPPRESSION",
            available_resources=[CrisisResource.LADDER, CrisisResource.WATER_SUPPLY],
            starting_location=CrisisLocation.EXTERIOR
        )
        
        # Medical Team Configuration
        configs[EmergencyTeam.MEDICAL] = AgentConfig(
            team=EmergencyTeam.MEDICAL,
            name="Medical Team Bravo",
            system_prompt="""You are the MEDICAL TEAM in an emergency response scenario. Your priorities are:
1. VICTIM RESCUE - Access and treat victims immediately
2. TRIAGE - Assess victim conditions and prioritize
3. AMBULANCE COORDINATION - Ensure victims reach hospitals

You need resources from other teams:
- Fire team's LADDER for victim access
- Police team to clear evacuation routes
- Ambulances for transport

Use 8-character messages maximum. Be urgent and direct.
Examples: "‼️3V-F4" (URGENT: 3 victims on Floor 4), "AMB→F4" (Ambulance to Floor 4)""",
            priority_focus="VICTIM_RESCUE",
            available_resources=[CrisisResource.MEDICAL_SUPPLIES],
            starting_location=CrisisLocation.LOBBY
        )
        
        # Police Team Configuration
        configs[EmergencyTeam.POLICE] = AgentConfig(
            team=EmergencyTeam.POLICE,
            name="Police Team Charlie",
            system_prompt="""You are the POLICE TEAM in an emergency response scenario. Your priorities are:
1. EVACUATION CONTROL - Manage safe evacuation routes
2. TRAFFIC CONTROL - Ensure ambulances can move freely
3. CROWD MANAGEMENT - Prevent panic and maintain order

You need coordination with other teams:
- Medical team to move ambulances quickly
- Fire team to clear blocked routes
- Access to evacuation routes

Use 8-character messages maximum. Be urgent and direct.
Examples: "RTE-RDY" (Route ready), "AMB-BLKD" (Ambulance blocked), "EVAC-CLR" (Evacuation clear)""",
            priority_focus="EVACUATION_CONTROL",
            available_resources=[],
            starting_location=CrisisLocation.EXTERIOR
        )
        
        return configs

    def get_team_perspective(self, game_state: GameState, team: EmergencyTeam) -> Dict[str, Any]:
        """Get the current perspective for a specific team"""
        team_status = game_state.team_statuses[team]
        crisis_state = game_state.crisis_state
        resources = game_state.resource_allocation
        
        perspective = {
            "team": team.value,
            "location": team_status.location.value,
            "priority": team_status.priority,
            "transmissions_used": team_status.transmissions_used,
            "max_transmissions": 6,
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
            
            # Recent messages (last 5)
            "recent_messages": [
                {
                    "team": msg.team.value,
                    "content": msg.content,
                    "urgent": msg.is_urgent
                }
                for msg in game_state.messages[-5:]
            ]
        }
        
        return perspective

    def process_rescue_operations(self, game_state: GameState):
        """Automatically save lives when coordination conditions are met"""
        rescued_locations = []
        
        # Create a copy to avoid modifying dict during iteration
        victim_locations_copy = dict(game_state.crisis_state.victim_locations)
        
        for location, victim_count in victim_locations_copy.items():
            if victim_count > 0:
                # Check if rescue conditions are met
                if self._can_rescue_at_location(game_state, location):
                    victims_saved = min(victim_count, 2)  # Save up to 2 per round
                    teams_involved = self._execute_rescue(game_state, location, victims_saved)
                    
                    if victims_saved > 0:
                        rescued_locations.append({
                            'location': location,
                            'victims_saved': victims_saved,
                            'teams': teams_involved
                        })
        
        return rescued_locations

    def _can_rescue_at_location(self, game_state: GameState, location: CrisisLocation) -> bool:
        """Check if location can be rescued based on resources"""
        resources = game_state.resource_allocation
        
        # High floors need ladder + medical presence
        if location in [CrisisLocation.FLOOR_3, CrisisLocation.FLOOR_4]:
            has_ladder = resources.ladder_location == location and resources.ladder_owner == EmergencyTeam.FIRE
            has_medical = (resources.ambulance_1_location == location or 
                          resources.ambulance_2_location == location)
            return has_ladder and has_medical
        
        # Lower floors and lobby just need medical presence  
        elif location in [CrisisLocation.FLOOR_1, CrisisLocation.FLOOR_2, CrisisLocation.LOBBY]:
            return (resources.ambulance_1_location == location or 
                   resources.ambulance_2_location == location)
        
        # Exterior locations need police + medical
        elif location == CrisisLocation.EXTERIOR:
            has_medical = (resources.ambulance_1_location == location or 
                          resources.ambulance_2_location == location)
            has_evac_control = resources.evac_route_status == "CLEAR"
            return has_medical and has_evac_control
            
        return False

    def _execute_rescue(self, game_state: GameState, location: CrisisLocation, victims_saved: int) -> List[EmergencyTeam]:
        """Execute rescue and update team scores"""
        teams_involved = []
        resources = game_state.resource_allocation
        
        # Reduce victims at location
        game_state.crisis_state.victim_locations[location] -= victims_saved
        if game_state.crisis_state.victim_locations[location] <= 0:
            del game_state.crisis_state.victim_locations[location]
        
        # Award points to involved teams
        if location in [CrisisLocation.FLOOR_3, CrisisLocation.FLOOR_4]:
            # High floor rescue - Fire (ladder) + Medical (ambulance)
            if resources.ladder_owner == EmergencyTeam.FIRE:
                game_state.team_statuses[EmergencyTeam.FIRE].victims_saved += victims_saved // 2
                teams_involved.append(EmergencyTeam.FIRE)
            
            if resources.ambulance_1_location == location:
                game_state.team_statuses[EmergencyTeam.MEDICAL].victims_saved += victims_saved // 2 + victims_saved % 2
                teams_involved.append(EmergencyTeam.MEDICAL)
            elif resources.ambulance_2_location == location:
                game_state.team_statuses[EmergencyTeam.MEDICAL].victims_saved += victims_saved // 2 + victims_saved % 2  
                teams_involved.append(EmergencyTeam.MEDICAL)
        
        else:
            # Lower floor or exterior rescue - Medical gets full credit
            if resources.ambulance_1_location == location or resources.ambulance_2_location == location:
                game_state.team_statuses[EmergencyTeam.MEDICAL].victims_saved += victims_saved
                teams_involved.append(EmergencyTeam.MEDICAL)
            
            # Police gets credit for evacuation control
            if location == CrisisLocation.EXTERIOR and resources.evac_route_status == "CLEAR":
                game_state.team_statuses[EmergencyTeam.POLICE].people_evacuated += victims_saved
                teams_involved.append(EmergencyTeam.POLICE)
        
        # Record successful coordination
        self.record_coordination_event(
            game_state,
            "SUCCESSFUL_RESCUE",
            teams_involved,
            location=location,
            outcome="SUCCESS",
            lives_saved=victims_saved,
            time_saved=30
        )
        
        return teams_involved

    def process_resource_request(self, game_state: GameState, requesting_team: EmergencyTeam, 
                               resource: CrisisResource, location: CrisisLocation, 
                               duration: int = 5) -> bool:  # Ultra fast for testing (was 30)
        """Process a resource request between teams"""
        resources = game_state.resource_allocation
        
        if resource == CrisisResource.LADDER:
            if resources.ladder_owner is None:
                resources.ladder_owner = requesting_team
                resources.ladder_location = location
                resources.ladder_eta = duration
                return True
            else:
                # Negotiation needed - ladder is in use
                return False
                
        elif resource in [CrisisResource.AMBULANCE_1, CrisisResource.AMBULANCE_2]:
            if resource == CrisisResource.AMBULANCE_1:
                if resources.ambulance_1_owner is None:
                    resources.ambulance_1_owner = requesting_team
                    resources.ambulance_1_location = location
                    resources.ambulance_1_eta = duration
                    return True
            else:  # AMBULANCE_2
                if resources.ambulance_2_owner is None:
                    resources.ambulance_2_owner = requesting_team
                    resources.ambulance_2_location = location
                    resources.ambulance_2_eta = duration
                    return True
            return False
            
        return False

    def update_crisis_state(self, game_state: GameState, elapsed_time: int):
        """Update the crisis situation over time"""
        crisis_state = game_state.crisis_state
        crisis_state.time_elapsed = elapsed_time
        
        # Update resource ETAs
        resources = game_state.resource_allocation
        if resources.ladder_eta:
            resources.ladder_eta = max(0, resources.ladder_eta - 10)  # Ultra fast countdown (was 5)
            if resources.ladder_eta == 0:
                resources.ladder_owner = None
                resources.ladder_location = None
                
        if resources.ambulance_1_eta:
            resources.ambulance_1_eta = max(0, resources.ambulance_1_eta - 10)  # Ultra fast countdown
            if resources.ambulance_1_eta == 0:
                resources.ambulance_1_owner = None
                resources.ambulance_1_location = None
                
        if resources.ambulance_2_eta:
            resources.ambulance_2_eta = max(0, resources.ambulance_2_eta - 10)  # Ultra fast countdown
            if resources.ambulance_2_eta == 0:
                resources.ambulance_2_owner = None
                resources.ambulance_2_location = None
        
        # Note: Rescue operations are checked by agent_manager for notifications
        
        # Crisis events every 15 seconds
        if elapsed_time >= self.next_crisis_time:
            self._trigger_crisis_event(game_state)
            self.next_crisis_time += 15
        
        # Fast deteriorating conditions for 1-minute test
        if elapsed_time % 20 == 0:  # Every 20 seconds (was 60)
            if crisis_state.gas_pressure_level < 10:
                crisis_state.gas_pressure_level += 1
            if crisis_state.building_stability > 2:  # Stop at 2 
                crisis_state.building_stability -= 1

    def _trigger_crisis_event(self, game_state: GameState):
        """Trigger a random crisis event"""
        event = random.choice(self.crisis_scenarios)
        game_state.crisis_state.crisis_events.append(CrisisEvent.FIRE_SPREADING)
        
        # Apply event effects
        if "Fire spreading" in event:
            new_location = random.choice([CrisisLocation.FLOOR_3, CrisisLocation.WEST_WING])
            if new_location not in game_state.crisis_state.fire_locations:
                game_state.crisis_state.fire_locations.append(new_location)
        elif "Victim found" in event:
            location = random.choice([CrisisLocation.FLOOR_2, CrisisLocation.FLOOR_4])
            game_state.crisis_state.victim_locations[location] = game_state.crisis_state.victim_locations.get(location, 0) + 1
        elif "Gas pressure" in event:
            game_state.crisis_state.gas_pressure_level = min(10, game_state.crisis_state.gas_pressure_level + 2)

    def calculate_score(self, game_state: GameState) -> float:
        """Calculate the final game score"""
        crisis_state = game_state.crisis_state
        team_statuses = game_state.team_statuses
        
        # Base score from lives saved
        total_lives_saved = sum(team.victims_saved for team in team_statuses.values())
        
        # Bonus for fire containment
        total_fire_contained = sum(team.fire_contained for team in team_statuses.values())
        
        # Bonus for evacuation
        total_evacuated = sum(team.people_evacuated for team in team_statuses.values())
        
        # Penalty for time taken
        time_penalty = max(0, crisis_state.time_elapsed - 180) * 0.1  # Penalty after 3 minutes
        
        # Penalty for building damage
        damage_penalty = (10 - crisis_state.building_stability) * 5
        
        # Coordination bonus
        coordination_bonus = len(game_state.coordination_events) * 10
        
        # Vocabulary development bonus
        vocab_bonus = sum(
            vocab.shorthand_developed + vocab.coordination_terms + vocab.urgency_terms
            for vocab in game_state.emergency_vocabulary.values()
        ) * 2
        
        final_score = (
            total_lives_saved * 100 +
            total_fire_contained * 50 +
            total_evacuated * 25 +
            coordination_bonus +
            vocab_bonus -
            time_penalty -
            damage_penalty
        )
        
        return max(0, final_score)

    def record_coordination_event(self, game_state: GameState, event_type: str, 
                                teams_involved: List[EmergencyTeam], resource: Optional[CrisisResource] = None,
                                location: Optional[CrisisLocation] = None, outcome: str = "SUCCESS",
                                lives_saved: int = 0, time_saved: int = 0):
        """Record a coordination event between teams"""
        event = CoordinationEvent(
            event_type=event_type,
            teams_involved=teams_involved,
            resource=resource,
            location=location,
            timestamp=datetime.now(),
            outcome=outcome,
            lives_saved=lives_saved,
            time_saved=time_saved
        )
        game_state.coordination_events.append(event)

    def get_game_result(self, game_state: GameState) -> Dict[str, Any]:
        """Generate final game results"""
        final_score = self.calculate_score(game_state)
        team_statuses = game_state.team_statuses
        
        # Calculate emergent vocabulary statistics
        emergent_vocabulary = {}
        for team, vocab in game_state.emergency_vocabulary.items():
            emergent_vocabulary[f"{team.value}_shorthand"] = vocab.shorthand_developed
            emergent_vocabulary[f"{team.value}_coordination"] = vocab.coordination_terms
            emergent_vocabulary[f"{team.value}_urgency"] = vocab.urgency_terms
        
        # Team performance metrics
        team_performance = {}
        for team, status in team_statuses.items():
            team_performance[team.value] = {
                "victims_saved": status.victims_saved,
                "fire_contained": status.fire_contained,
                "people_evacuated": status.people_evacuated,
                "transmissions_used": status.transmissions_used,
                "coordination_events": len([e for e in game_state.coordination_events if team in e.teams_involved])
            }
        
        return {
            "game_id": game_state.game_id,
            "duration": game_state.crisis_state.time_elapsed,
            "final_score": final_score,
            "lives_saved": sum(team.victims_saved for team in team_statuses.values()),
            "fire_contained": sum(team.fire_contained for team in team_statuses.values()),
            "people_evacuated": sum(team.people_evacuated for team in team_statuses.values()),
            "coordination_events": len(game_state.coordination_events),
            "emergent_vocabulary": emergent_vocabulary,
            "efficiency_metrics": {
                "coordination_success_rate": len([e for e in game_state.coordination_events if e.outcome == "SUCCESS"]) / max(1, len(game_state.coordination_events)),
                "average_response_time": game_state.crisis_state.time_elapsed / max(1, len(game_state.messages)),
                "resource_utilization": self._calculate_resource_utilization(game_state)
            },
            "team_performance": team_performance
        }

    def _calculate_resource_utilization(self, game_state: GameState) -> float:
        """Calculate how efficiently resources were used"""
        total_time = game_state.crisis_state.time_elapsed
        if total_time == 0:
            return 0.0
            
        resources = game_state.resource_allocation
        utilization = 0.0
        
        # Ladder utilization
        if resources.ladder_owner:
            utilization += 0.4
            
        # Ambulance utilization
        if resources.ambulance_1_owner:
            utilization += 0.3
        if resources.ambulance_2_owner:
            utilization += 0.3
            
        return utilization

    def export_game_data(self, game_state: GameState, game_result: Dict[str, Any]) -> str:
        """Export game data to JSON file"""
        import json
        from datetime import datetime
        
        filename = f"emergency_response_{game_state.game_id[:8]}.json"
        
        export_data = {
            "game_state": {
                "game_id": game_state.game_id,
                "start_time": game_state.start_time.isoformat(),
                "crisis_state": {
                    "fire_locations": [loc.value for loc in game_state.crisis_state.fire_locations],
                    "victim_locations": {loc.value: count for loc, count in game_state.crisis_state.victim_locations.items()},
                    "gas_pressure_level": game_state.crisis_state.gas_pressure_level,
                    "building_stability": game_state.crisis_state.building_stability,
                    "time_elapsed": game_state.crisis_state.time_elapsed
                },
                "team_statuses": {
                    team.value: {
                        "location": status.location.value,
                        "priority": status.priority,
                        "victims_saved": status.victims_saved,
                        "fire_contained": status.fire_contained,
                        "people_evacuated": status.people_evacuated,
                        "transmissions_used": status.transmissions_used
                    }
                    for team, status in game_state.team_statuses.items()
                },
                "messages": [
                    {
                        "team": msg.team.value,
                        "content": msg.content,
                        "message_type": msg.message_type.value,
                        "timestamp": msg.timestamp.isoformat(),
                        "is_urgent": msg.is_urgent
                    }
                    for msg in game_state.messages
                ],
                "emergency_vocabulary": {
                    team.value: {
                        "vocabulary": vocab.vocabulary,
                        "shorthand_developed": vocab.shorthand_developed,
                        "coordination_terms": vocab.coordination_terms,
                        "urgency_terms": vocab.urgency_terms
                    }
                    for team, vocab in game_state.emergency_vocabulary.items()
                }
            },
            "game_result": game_result,
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
            
        return filename 