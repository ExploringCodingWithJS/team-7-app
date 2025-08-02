# 🚨 Three-Team Emergency Response - Emergent Communication Study

A multi-agent system where **3 emergency response teams** must coordinate during a crisis scenario using **12-character emergency radio protocol**. The goal is to observe how agents spontaneously develop their own language and coordination patterns under extreme time pressure.

## ⚡ **ULTRA-FAST TEST MODE ENABLED** ⚡
```
🎯 DURATION: 1 minute (was 5 minutes)
🚀 AGENT RESPONSES: Every 0.5 seconds (was 3 seconds)
💬 MESSAGE LIMIT: 50 per team (was 12)
⏱️ COOLDOWN: 0.01 seconds (was 0.1)
🏥 RESCUE CHECKS: Every 0.5 seconds
🚨 CRISIS EVENTS: Every 15 seconds
📊 STATUS UPDATES: Every 15 seconds
🎯 WIN CONDITION: 40% victims saved (was 60%)
```

## 🎯 Core Concept

**Three emergency response teams** must coordinate during a major apartment building explosion:

- **🔥 Fire Team**: Rescue equipment, fire suppression, hazmat gear
- **🚑 Medical Team**: Paramedics, ambulances, medical supplies, trauma equipment  
- **👮 Police Team**: Evacuation support, traffic control, crowd barriers, investigation units

## 🎮 Game Mechanics

### **🏗️ Game Structure** (⚡ ULTRA-FAST TEST MODE)
- **Duration**: 1 minute (60 seconds) - ⚡ SPEED TEST MODE
- **Teams**: 3 autonomous AI agents (Fire 🔥, Medical 🚑, Police 👮)
- **Location**: 4-floor apartment building with explosion damage
- **Objective**: Maximize lives saved through coordinated emergency response

### **🚨 Initial Crisis State**
```
Fire Locations: Floor 2, East Wing
Victim Locations: 
  - Floor 3: 2 victims
  - Floor 4: 1 victim  
  - Lobby: 3 victims
Blocked Routes: Floor 1 (debris)
Gas Pressure: 3/10 (rising)
Building Stability: 7/10 (deteriorating)
```

### **👥 Team Roles & Priorities**

#### **🔥 Fire Team**
- **Location**: Exterior (starting position)
- **Resources**: Heavy Rescue Ladder, Water Supply
- **Priority**: Fire suppression → Structure safety → Victim rescue
- **Capabilities**: Control fires, assess building stability, ladder rescue operations

#### **🚑 Medical Team** 
- **Location**: Lobby (starting position)
- **Resources**: Medical supplies
- **Priority**: Victim rescue → Triage → Hospital transport
- **Capabilities**: Treat victims, coordinate ambulances, medical assessment

#### **👮 Police Team**
- **Location**: Exterior (starting position) 
- **Resources**: None (coordination role)
- **Priority**: Evacuation control → Traffic management → Route clearing
- **Capabilities**: Manage evacuation routes, coordinate ambulance access, crowd control

### **🏗️ Critical Resource Constraints**

#### **🪜 Heavy Rescue Ladder**
- **Owned by**: Fire Team initially
- **Required for**: High-floor victim access (F3, F4)
- **Negotiation**: Medical team needs ladder for victim rescue
- **Usage time**: 60 seconds default, then becomes available

#### **🚑 Ambulances (2 available)**
- **Ambulance 1 & 2**: Not initially assigned
- **Required for**: Victim transport to hospitals
- **Controlled by**: Any team can request
- **Conflict**: Limited availability creates competition

#### **🛣️ Evacuation Routes**
- **Status**: Initially blocked
- **Controlled by**: Police team
- **Impact**: Affects ambulance movement and crowd evacuation

### **📡 Communication System**

#### **12-Character Message Limit** (✅ UPDATED)
```
Valid Examples:
"L→SUPR-F4?"   (Ladder for suppression Floor 4?)
"‼️3VICTIM-F4" (URGENT: 3 victims Floor 4)
"AMB1→F4-GO"   (Ambulance 1 to Floor 4, go)
"RTE-CLEAR"    (Route clear)  
"F3✓SAVED2V"   (Floor 3 clear, saved 2 victims)
"EVAC-READY"   (Evacuation ready)
"COORD-OK"     (Coordination okay)
```

#### **Transmission Limits** (⚡ ULTRA-FAST TEST MODE)
- **Max per team**: 50 transmissions total (unlimited for testing)
- **Cooldown**: 0.01 seconds between messages (almost none)
- **Agent frequency**: Responds every 0.5 seconds (ultra-fast)
- **Radio interference**: Random 0.01-0.05s delays (minimal)

#### **Message Types Detected**
- **Resource Request**: Contains "?" (e.g., "L→F4?")
- **Urgent Alert**: Contains "‼️" or "!" 
- **Coordination**: Contains "RTE", "EVAC", "CLEAR", "COORD"
- **Status Update**: General information sharing

### **⏰ Dynamic Crisis Events**

#### **Crisis Updates** (⚡ ULTRA-FAST - Every 15 seconds)
```
🚨FLASH#1: Fire spreading to east wing
🚨FLASH#2: Victim found on floor 3  
🚨FLASH#3: Gas pressure building
🚨FLASH#4: Structure collapse on floor 2
🚨FLASH#5: Ambulance arrival delayed
🚨FLASH#6: Evac route blocked by debris
```

#### **Deteriorating Conditions** (⚡ ULTRA-FAST TEST MODE)
- **Gas Pressure**: Increases by 1 every 20 seconds (fast escalation)
- **Building Stability**: Decreases by 1 every 20 seconds, stops at 2
- **Resource ETAs**: Count down 10x faster (5-second deployments)
- **Status Updates**: Every 15 seconds (was 60)

### **🎯 Scoring System**

#### **Point Values**
- **Lives Saved**: +100 points each
- **Fire Contained**: +50 points per location
- **People Evacuated**: +25 points each
- **Coordination Events**: +10 points each
- **Emergent Vocabulary**: +2 points per new term

#### **Penalties**
- **Time Penalty**: -0.1 points per second after 3 minutes
- **Building Damage**: -5 points per stability point lost
- **Failed Coordination**: Reduces efficiency bonuses

#### **Bonuses**
- **Successful Resource Sharing**: Coordination event bonuses
- **Vocabulary Development**: Points for shorthand creation
- **Quick Response**: Time-based efficiency bonuses

## 📡 Expected Emergent Language

**Resource requests:** `L→F3?` (Ladder to Floor 3?)
**Status:** `F3✓2V` (Floor 3 clear, 2 victims found)  
**Urgent:** `‼️AMB` (URGENT: Need ambulance)
**Coordination:** `RTE-CLR` (Route cleared)
**Priorities:** `F>R` (Fire suppression before rescue) or `R>F` (Rescue before fire)

## 🏗️ Architecture

### **Core Components**
- **`models.py`**: Data structures for emergency teams, crisis state, resources
- **`game_engine.py`**: Crisis simulation, resource allocation, scoring
- **`agent.py`**: Emergency team agents with 8-character message generation
- **`agent_manager.py`**: Orchestrates the three-team coordination
- **`slack_integration.py`**: Real-time communication with Slack
- **`main.py`**: System entry point and initialization

### **Emergent Communication Features**
- **8-character limit enforcement** with LLM prompting
- **Resource negotiation tracking** between teams
- **Vocabulary development monitoring** for each team
- **Coordination event recording** for analysis
- **Urgency detection** and priority handling

### **Research Goals**
- **Emergent shorthand**: How teams develop abbreviations under pressure
- **Resource negotiation language**: How teams request and share limited resources
- **Urgency communication**: How teams signal and respond to critical situations
- **Coordination patterns**: How teams develop protocols for working together
- **Time pressure effects**: How communication evolves under 5-minute constraint

## 🚀 Quick Start

### **1. Environment Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp env_example.txt .env
```

### **2. Slack App Configuration**
1. Create a Slack app at https://api.slack.com/apps
2. Enable **Socket Mode**
3. Add **Event Subscriptions** with these events:
   - `message.channels` (for reading messages)
   - `app_mention` (for bot mentions)
4. Add **OAuth Scopes**:
   - `chat:write` (send messages)
   - `channels:history` (read messages)
   - `app_mentions:read` (read mentions)
5. Install app to workspace
6. Copy tokens to `.env` file

### **3. API Keys**
```bash
# .env file
OPENROUTER_API_KEY=your_openrouter_key_here
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
SLACK_CHANNEL_ID=C1234567890
```

### **4. Run the System**
```bash
python main.py
```

### **5. Start a Game**
In your Slack channel, type: `<START_GAME>`

## 📊 Detailed Game Flow

### **🚀 Phase 1: Initial Response (0-10 seconds)** ⚡ ULTRA-FAST
1. **Game Initialization**: 
   - 3 AI agents spawn at starting locations
   - Crisis state established (fires, victims, blocked routes)
   - Resource allocation initialized (ladder with Fire team)

2. **Situation Assessment**:
   - Teams receive full crisis briefing
   - Each team evaluates priorities based on role
   - Initial communication begins (0.5-second intervals)

### **⚡ Phase 2: Active Coordination (10-50 seconds)** ⚡ SPEED TEST
1. **Resource Negotiation Cycle**:
   ```
   Medical: "‼️3V-F4"  (Urgent: 3 victims Floor 4)
   Fire: "L→SUPR?"     (Ladder for suppression?)
   Medical: "L→F4?"    (Ladder to Floor 4?)
   Fire: "L→F4-1MIN"   (Ladder to F4, 1 minute)
   Police: "RTE-CLR"   (Route clearing)
   ```

2. **Dynamic Crisis Events** (Every 2 minutes):
   - New victims discovered
   - Fire spreading to new areas
   - Gas pressure increasing
   - Route blockages changing

3. **Resource State Updates**:
   - Ladder assignments and ETAs
   - Ambulance availability
   - Route status changes

### **🏁 Phase 3: Final Push (50-60 seconds)** ⚡ SPRINT FINISH
1. **Escalating Urgency**:
   - Gas pressure near maximum (8-10/10)
   - Building stability critical (1-3/10)  
   - Ultra-fast agent responses (0.5-second intervals)

2. **Last-Minute Coordination**:
   - Teams prioritize highest-impact actions
   - Resource sharing becomes critical (5-second deployments)
   - Emergency vocabulary reaches peak development

### **📈 Real-Time Monitoring**

#### **Status Updates (Every 15 seconds)** ⚡ ULTRA-FAST
```
📊 STATUS UPDATE 📊
Time: 0:45 remaining
🔥 Fire: 2 contained | 🚑 Victims: 3 saved | 👮 Evacuated: 5
Coordination events: 4
```

#### **Resource Conflict Resolution**
```
✅ RESOURCE GRANTED: FIRE gets ladder at FLOOR_4
❌ AMBULANCE 1: Already in use
⏳ LADDER ETA: 45 seconds remaining
```

### **🧠 AI Agent Decision Making**

#### **Response Triggers** (Agents respond when):
- **Urgent situation detected**: Gas ≥7, Stability ≤3, Victims ≥3
- **Direct request received**: Mentioned in recent messages
- **Resource conflict**: Their resources requested by others
- **Random threshold**: Based on urgency_threshold (0.7)

#### **Message Generation Process**:
1. **Situation Analysis**: Current crisis state + recent messages
2. **Priority Assessment**: Team role vs immediate needs
3. **LLM Prompt**: System prompt + current situation context
4. **12-Character Constraint**: Message parsed and validated (✅ UPDATED)
5. **Vocabulary Tracking**: New terms recorded for research

### **🎉 NEW: Automatic Rescue System**

#### **Rescue Conditions** (✅ FIXED: Now rescues actually work!)
- **High Floors (F3, F4)**: Requires Fire ladder + Medical ambulance at same location
- **Lower Floors (F1, F2, Lobby)**: Requires Medical ambulance at location
- **Exterior**: Requires Medical ambulance + Police-controlled clear evacuation route

#### **Rescue Process** (⚡ ULTRA-FAST):
1. **Automatic Detection**: Every 0.5 seconds, system checks rescue conditions
2. **Victim Saving**: Up to 2 victims saved per location per round
3. **Team Credit**: Points awarded to teams involved in coordination
4. **Immediate Feedback**: Success notifications sent to Slack instantly
5. **Progress Tracking**: Victims removed from crisis state when saved
6. **Win Condition**: 40% victims saved = SUCCESS (lowered for speed test)

#### **Success Notifications**:
```
🎉 **RESCUE SUCCESS!** 🎉
📍 F4: 2 victims saved!
👥 Teams: FIRE + MEDICAL
⚡ Excellent coordination!
```

### **🔬 Emergent Behavior Patterns**

#### **Vocabulary Development**:
- **Shorthand Creation**: "L→F4" (Ladder to Floor 4)
- **Urgency Signaling**: "‼️" prefix for critical situations
- **Coordination Terms**: "RTE", "COORD", "SHARE"
- **Location Codes**: "F1-F4", "EW", "WW", "LB", "EXT"

#### **Communication Patterns**:
- **Resource Requests**: Question format "L→F4?"
- **Status Updates**: Confirmation format "F3✓2V" 
- **Urgent Alerts**: Exclamation format "‼️GAS-HIGH"
- **Coordination**: Action format "RTE-CLR"

## 🔍 Monitoring & Analysis

### **Real-time Metrics**
- **Lives saved** by each team
- **Fire containment** progress
- **Evacuation** success rate
- **Coordination events** frequency
- **Emergent vocabulary** development

### **Post-Game Analysis**
- **Communication patterns** analysis
- **Resource utilization** efficiency
- **Team coordination** success rates
- **Vocabulary evolution** tracking
- **Time pressure effects** on communication

## 📈 Expected Outcomes

### **Emergent Behaviors**
- **Shorthand development**: Teams create abbreviations for efficiency
- **Resource negotiation**: Teams develop protocols for sharing limited resources
- **Urgency signaling**: Teams develop ways to signal critical situations
- **Coordination protocols**: Teams establish working relationships

### **Research Insights**
- **Communication efficiency** under time pressure
- **Resource allocation** strategies in crisis situations
- **Team coordination** patterns in emergency response
- **Language evolution** in constrained environments

## 🛠️ Technical Details

### **LLM Integration**
- **OpenRouter API** with Claude 3.5 Sonnet for agent intelligence
- **Temperature 0.7** for creative but consistent responses
- **8-character limit** enforced through prompting
- **Context window** includes recent messages and crisis state

### **Slack Integration**
- **Socket Mode** for real-time communication
- **Rate limiting** to respect Slack API limits
- **Message deduplication** to prevent processing duplicates
- **Error handling** for robust operation

### **Game Engine**
- **5-minute time limit** with crisis events
- **Resource allocation** simulation
- **Scoring system** based on lives saved and efficiency
- **Data export** for analysis

## 📝 Sample Game Session

```
🚨 EMERGENCY RESPONSE MISSION STARTED 🚨
3 emergency teams deployed to apartment building explosion.
5 minutes to coordinate and save lives!
Teams: Fire 🔥 | Medical 🚑 | Police 👮
START COORDINATING!

🔥 FIRE: L→SUPR?
🚑 MEDICAL: ‼️3V-F4
🔥 FIRE: L→F4-1MIN
👮 POLICE: RTE-RDY
🚑 MEDICAL: AMB→F4
👮 POLICE: AMB-BLKD
🚨 CRISIS UPDATE 🚨
🚨FLASH#2: Victim found on floor 3
Time: 2:30 | Gas: 5/10 | Building: 6/10

📊 STATUS UPDATE 📊
Time: 3:45 remaining
🔥 Fire: 2 contained | 🚑 Victims: 3 saved | 👮 Evacuated: 5
Coordination events: 4
```

## 🔬 Research Applications

This system is designed for studying:
- **Emergent communication** in multi-agent systems
- **Resource coordination** under constraints
- **Time pressure effects** on language development
- **Emergency response** coordination patterns
- **Multi-agent negotiation** strategies

## 🛠️ Iteration & Customization Guide

### **🎛️ Easy Configuration Changes**

#### **Game Parameters** (`main.py` & `agent_manager.py`)
```python
# Timing Configuration
self.observation_interval = 5      # Agent response frequency (seconds)
self.game_duration = 300          # Total game time (seconds)
self.crisis_update_interval = 120  # Crisis events frequency (seconds)

# Agent Limits
max_transmissions = 6             # Messages per team
transmission_cooldown = 0.3       # Cooldown between messages
urgency_threshold = 0.7           # Response probability
```

#### **Crisis Scenarios** (`game_engine.py`)
```python
# Add new crisis events
self.crisis_scenarios = [
    "🚨FLASH#7: Chemical leak detected",
    "🚨FLASH#8: Second explosion imminent",
    "🚨FLASH#9: Power grid failure",
    # Add your scenarios here
]
```

#### **Team Configurations** (`game_engine.py`)
```python
# Modify team priorities and resources
configs[EmergencyTeam.FIRE] = AgentConfig(
    priority_focus="FIRE_SUPPRESSION",  # Change focus
    available_resources=[...],          # Modify resources
    urgency_threshold=0.8,             # Adjust responsiveness
)
```

### **🔧 Advanced Modifications**

#### **New Team Types** (`models.py`)
```python
class EmergencyTeam(Enum):
    FIRE = "FIRE"
    MEDICAL = "MEDICAL" 
    POLICE = "POLICE"
    HAZMAT = "HAZMAT"        # Add new team
    RESCUE = "RESCUE"        # Add specialized rescue
```

#### **Additional Resources** (`models.py`)
```python
class CrisisResource(Enum):
    LADDER = "LADDER"
    AMBULANCE_1 = "AMBULANCE_1"
    DRONE = "DRONE"              # Add surveillance drone
    HELICOPTER = "HELICOPTER"    # Add medical helicopter
    HAZMAT_SUIT = "HAZMAT_SUIT"  # Add specialized equipment
```

#### **New Locations** (`models.py`)
```python
class CrisisLocation(Enum):
    BASEMENT = "BSM"     # Add basement level
    ROOF = "ROOF"        # Add rooftop access
    PARKING = "PKG"      # Add parking garage
```

### **📊 Scoring Modifications** (`game_engine.py`)
```python
def calculate_score(self, game_state: GameState) -> float:
    # Modify point values
    total_lives_saved * 150        # Increase life value
    + coordination_bonus * 15      # Increase coordination value
    + new_metric_bonus * 25        # Add new scoring criteria
```

### **🤖 AI Behavior Tuning**

#### **Response Triggers** (`agent.py`)
```python
def _should_respond(self, game_state, recent_messages) -> bool:
    # Add new response conditions
    if self._has_equipment_failure():
        return True
    if self._detects_secondary_threat():
        return True
    # Customize decision logic
```

#### **Message Parsing** (`agent.py`)
```python
def _determine_message_type(self, content: str) -> MessageType:
    # Add new message patterns
    if "EVAC" in content_upper:
        return MessageType.EVACUATION_ORDER
    if "HAZMAT" in content_upper:
        return MessageType.HAZMAT_ALERT
```

### **🎯 Research Extensions**

#### **Communication Analysis**
- Track message evolution over time
- Analyze response patterns by crisis severity
- Study vocabulary convergence between teams
- Measure coordination efficiency metrics

#### **Scenario Variations**
- **Building Types**: Hospital, school, office tower
- **Crisis Types**: Chemical spill, earthquake, terrorist attack
- **Weather**: Wind affecting fire spread, rain impacting visibility
- **Time of Day**: Daylight vs nighttime operations

#### **Multi-Game Studies**
- Run 100+ games with same configuration
- Analyze emergent vocabulary consistency
- Study adaptation to recurring scenarios
- Compare human vs AI coordination patterns

### **🔌 Integration Extensions**

#### **Real Human Participation**
```python
# Allow human players to join as team members
class HumanTeamAgent(EmergencyTeamAgent):
    async def generate_response(self, game_state, recent_messages):
        # Wait for human input via Slack
        return await self.wait_for_human_input()
```

#### **External Data Sources**
```python
# Integrate real emergency protocols
def load_emergency_protocols(self):
    # Load actual fire department SOPs
    # Integrate medical triage protocols
    # Use real resource allocation data
```

#### **Advanced Analytics**
```python
# Export to research databases
def export_research_data(self, game_state, results):
    # Export to PostgreSQL/MongoDB
    # Generate statistical reports
    # Create visualization dashboards
```

### **📈 Performance Optimization**

#### **Parallel Game Sessions**
```python
# Run multiple games simultaneously
async def run_parallel_games(num_games: int):
    tasks = [self.start_game() for _ in range(num_games)]
    results = await asyncio.gather(*tasks)
    return self.analyze_batch_results(results)
```

#### **LLM Model Comparison**
```python
# Test different models via OpenRouter
models = [
    "anthropic/claude-3.5-sonnet",
    "openai/gpt-4-turbo", 
    "meta-llama/llama-3.1-70b"
]
# Compare communication patterns across models
```

## 🔧 **CRITICAL FIXES: Making Rescues Actually Work**

### **✅ FIXES IMPLEMENTED**
🎉 **The game now actually saves victims!** Here's what was changed:

1. **✅ Added Automatic Rescue Logic**: Teams automatically save victims when they coordinate resources properly
2. **✅ Increased Message Limits**: 8→12 characters, 6→12 transmissions per team  
3. **✅ Faster Response Times**: 5→3 second intervals, 0.3→0.1 second cooldowns
4. **✅ Slower Crisis Escalation**: 30→60 second deterioration, building stops at stability 2
5. **✅ Immediate Success Feedback**: Real-time rescue success notifications
6. **✅ Clear Win Conditions**: Success at 60% victims saved (was 100%)

### **❌ Previous Problems (Now Fixed)**
1. ~~**No Rescue Logic**: Teams coordinate but no lives are actually saved~~ ✅ **FIXED**
2. ~~**Resource Allocation Dead End**: Getting resources doesn't trigger rescues~~ ✅ **FIXED**
3. ~~**Too Many Constraints**: 8-character limit + 6 message limit + complex coordination~~ ✅ **FIXED**
4. ~~**No Success Feedback**: Agents don't know when they succeed~~ ✅ **FIXED**
5. ~~**Escalating Crisis**: Conditions worsen faster than teams can respond~~ ✅ **FIXED**

### **✅ Proposed Solutions**

#### **1. Add Automatic Rescue Logic** (`game_engine.py`)
```python
def process_rescue_operations(self, game_state: GameState):
    """Automatically save lives when coordination conditions are met"""
    for location, victim_count in game_state.crisis_state.victim_locations.items():
        if victim_count > 0:
            # Check if rescue conditions are met
            if self._can_rescue_at_location(game_state, location):
                victims_saved = min(victim_count, 2)  # Save up to 2 per round
                self._execute_rescue(game_state, location, victims_saved)
                
def _can_rescue_at_location(self, game_state: GameState, location: CrisisLocation) -> bool:
    """Check if location can be rescued based on resources"""
    resources = game_state.resource_allocation
    
    # High floors need ladder + medical presence
    if location in [CrisisLocation.FLOOR_3, CrisisLocation.FLOOR_4]:
        return (resources.ladder_location == location and 
                (resources.ambulance_1_location == location or 
                 resources.ambulance_2_location == location))
    
    # Lower floors just need medical presence  
    return (resources.ambulance_1_location == location or 
            resources.ambulance_2_location == location)
```

#### **2. Reduce Communication Barriers**
```python
# In agent.py - Increase message limits
max_transmissions = 12        # Double the messages (was 6)
message_length_limit = 12     # Increase from 8 to 12 characters
transmission_cooldown = 0.1   # Faster responses (was 0.3)

# In agent_manager.py - More frequent responses
observation_interval = 3      # Check every 3 seconds (was 5)
```

#### **3. Slower Crisis Escalation**
```python
# In game_engine.py - Make conditions deteriorate slower
if elapsed_time % 60 == 0:    # Every 60 seconds (was 30)
    if crisis_state.gas_pressure_level < 10:
        crisis_state.gas_pressure_level += 1
    if crisis_state.building_stability > 2:  # Stop at 2 (was 0)
        crisis_state.building_stability -= 1
```

#### **4. More Resources Available**
```python
# Add third ambulance and faster response times
class CrisisResource(Enum):
    LADDER = "LADDER"
    AMBULANCE_1 = "AMBULANCE_1"  
    AMBULANCE_2 = "AMBULANCE_2"
    AMBULANCE_3 = "AMBULANCE_3"  # Add third ambulance
    QUICK_RESPONSE = "QUICK_RESPONSE"  # Faster team for easy rescues

# Reduce resource usage time
default_resource_duration = 30  # Was 60 seconds
```

#### **5. Success Feedback Loop**
```python
async def _send_rescue_success(self, location: CrisisLocation, victims_saved: int, teams_involved: List[EmergencyTeam]):
    """Send immediate feedback when rescues succeed"""
    team_names = " + ".join([team.value for team in teams_involved])
    await self.slack_integration.send_message(
        f"🎉 **RESCUE SUCCESS!** 🎉\n"
        f"📍 {location.value}: {victims_saved} victims saved!\n"
        f"👥 Teams: {team_names}\n"
        f"⚡ Great coordination!"
    )
```

#### **6. Simplified Win Conditions**
```python
# Make it easier to "win" a scenario
def check_scenario_success(self, game_state: GameState) -> bool:
    """Check if teams have achieved a successful rescue scenario"""
    total_saved = sum(team.victims_saved for team in game_state.team_statuses.values())
    total_victims = sum(game_state.crisis_state.victim_locations.values())
    
    # Success if 60% of victims saved (was 100%)
    return total_saved >= (total_victims * 0.6)
```

### **🚀 Quick Implementation Priority**

**Immediate Changes (30 minutes):**
1. Add automatic rescue logic when resources align
2. Increase message limits (6→12) and length (8→12 chars)  
3. Add rescue success notifications
4. Slower crisis deterioration

**Next Phase (1 hour):**
5. Add third ambulance resource
6. Implement win condition checks
7. Add rescue attempt tracking
8. Better coordination event scoring

**Testing Phase:**
9. Run test games to verify rescues work
10. Adjust timing and difficulty based on results

This should make the game actually **winnable** while preserving the emergent communication research goals!

## 📄 License

This project is for research purposes. Please ensure compliance with Anthropic and Slack API terms of service. 