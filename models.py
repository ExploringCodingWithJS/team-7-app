from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from pydantic import BaseModel, Field
from datetime import datetime

class EmergencyTeam(Enum):
    FIRE = "FIRE"
    MEDICAL = "MEDICAL" 
    POLICE = "POLICE"

class CrisisResource(Enum):
    LADDER = "LADDER"
    AMBULANCE_1 = "AMBULANCE_1"
    AMBULANCE_2 = "AMBULANCE_2"
    EVAC_ROUTE = "EVAC_ROUTE"
    WATER_SUPPLY = "WATER_SUPPLY"
    MEDICAL_SUPPLIES = "MEDICAL_SUPPLIES"

class CrisisLocation(Enum):
    FLOOR_1 = "F1"
    FLOOR_2 = "F2"
    FLOOR_3 = "F3"
    FLOOR_4 = "F4"
    EAST_WING = "EW"
    WEST_WING = "WW"
    LOBBY = "LB"
    EXTERIOR = "EXT"

class CrisisEvent(Enum):
    FIRE_SPREADING = "FIRE_SPREADING"
    VICTIM_FOUND = "VICTIM_FOUND"
    GAS_PRESSURE = "GAS_PRESSURE"
    STRUCTURE_COLLAPSE = "STRUCTURE_COLLAPSE"
    AMBULANCE_ARRIVAL = "AMBULANCE_ARRIVAL"
    EVAC_ROUTE_BLOCKED = "EVAC_ROUTE_BLOCKED"

class MessageType(Enum):
    RESOURCE_REQUEST = "resource_request"
    STATUS_UPDATE = "status_update"
    URGENT_ALERT = "urgent_alert"
    COORDINATION = "coordination"
    PRIORITY_NEGOTIATION = "priority_negotiation"
    CRISIS_UPDATE = "crisis_update"

class CrisisState(BaseModel):
    """Current state of the crisis situation"""
    fire_locations: List[CrisisLocation] = Field(default_factory=list)
    victim_locations: Dict[CrisisLocation, int] = Field(default_factory=dict)
    blocked_routes: List[CrisisLocation] = Field(default_factory=list)
    gas_pressure_level: int = Field(default=0, ge=0, le=10)
    building_stability: int = Field(default=7, ge=0, le=10)
    time_elapsed: int = Field(default=0)  # in seconds
    crisis_events: List[CrisisEvent] = Field(default_factory=list)

class ResourceAllocation(BaseModel):
    """Current allocation of crisis resources"""
    ladder_location: Optional[CrisisLocation] = None
    ladder_owner: Optional[EmergencyTeam] = None
    ladder_eta: Optional[int] = None  # seconds until available
    
    ambulance_1_location: Optional[CrisisLocation] = None
    ambulance_1_owner: Optional[EmergencyTeam] = None
    ambulance_1_eta: Optional[int] = None
    
    ambulance_2_location: Optional[CrisisLocation] = None
    ambulance_2_owner: Optional[EmergencyTeam] = None
    ambulance_2_eta: Optional[int] = None
    
    evac_route_status: str = "BLOCKED"  # "CLEAR", "BLOCKED", "PARTIAL"
    evac_route_controller: Optional[EmergencyTeam] = None

class TeamStatus(BaseModel):
    """Status of each emergency team"""
    team: EmergencyTeam
    location: CrisisLocation
    resources_available: List[CrisisResource]
    priority: str  # Current team priority
    victims_saved: int = 0
    fire_contained: int = 0
    people_evacuated: int = 0
    transmissions_used: int = 0
    last_transmission_time: Optional[datetime] = None

class Message(BaseModel):
    """Emergency communication message (12-character limit)"""
    team: EmergencyTeam
    content: str = Field(max_length=12)  # Increased from 8 to 12 characters
    message_type: MessageType
    timestamp: datetime
    is_urgent: bool = False
    target_team: Optional[EmergencyTeam] = None
    location: Optional[CrisisLocation] = None

class CoordinationEvent(BaseModel):
    """Record of coordination events between teams"""
    event_type: str
    teams_involved: List[EmergencyTeam]
    resource: Optional[CrisisResource] = None
    location: Optional[CrisisLocation] = None
    timestamp: datetime
    outcome: str
    lives_saved: int = 0
    time_saved: int = 0  # seconds

class EmergencyVocabulary(BaseModel):
    """Emergent vocabulary developed by teams"""
    team: EmergencyTeam
    vocabulary: Dict[str, str] = Field(default_factory=dict)
    shorthand_developed: int = 0
    coordination_terms: int = 0
    urgency_terms: int = 0

class GameState(BaseModel):
    """Overall game state for the emergency response scenario"""
    game_id: str
    start_time: datetime
    crisis_state: CrisisState
    resource_allocation: ResourceAllocation
    team_statuses: Dict[EmergencyTeam, TeamStatus]
    messages: List[Message] = Field(default_factory=list)
    coordination_events: List[CoordinationEvent] = Field(default_factory=list)
    emergency_vocabulary: Dict[EmergencyTeam, EmergencyVocabulary] = Field(default_factory=dict)
    game_phase: str = "INITIAL_RESPONSE"
    total_lives_saved: int = 0
    total_fire_contained: int = 0
    total_evacuated: int = 0
    game_duration: int = 60  # 1 minute in seconds (was 300)

class AgentConfig(BaseModel):
    """Configuration for each emergency team agent"""
    team: EmergencyTeam
    name: str
    system_prompt: str
    priority_focus: str
    available_resources: List[CrisisResource]
    starting_location: CrisisLocation
    response_delay_range: Tuple[float, float] = (0.1, 0.5)
    urgency_threshold: float = 0.7
    coordination_priority: float = 0.8
    max_transmissions: int = 50  # Unlimited for testing (was 12)
    transmission_cooldown: float = 0.01  # Almost no cooldown (was 0.1)

class GameResult(BaseModel):
    """Results of the emergency response game"""
    game_id: str
    duration: int
    final_score: float
    lives_saved: int
    fire_contained: int
    people_evacuated: int
    coordination_events: int
    emergent_vocabulary: Dict[str, int]
    efficiency_metrics: Dict[str, Any]
    team_performance: Dict[EmergencyTeam, Dict[str, Any]] 