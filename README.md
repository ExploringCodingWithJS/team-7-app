# 🚨 Three-Team Emergency Response - Emergent Communication Study

A multi-agent system where **3 emergency response teams** must coordinate during a crisis scenario using **8-character emergency radio protocol**. The goal is to observe how agents spontaneously develop their own language and coordination patterns under extreme time pressure.

## 🎯 Core Concept

**Three emergency response teams** must coordinate during a major apartment building explosion:

- **🔥 Fire Team**: Rescue equipment, fire suppression, hazmat gear
- **🚑 Medical Team**: Paramedics, ambulances, medical supplies, trauma equipment  
- **👮 Police Team**: Evacuation support, traffic control, crowd barriers, investigation units

## 🎮 Game Mechanics

### **🏗️ Game Structure**
- **Duration**: 5 minutes (300 seconds)
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

#### **8-Character Message Limit**
```
Valid Examples:
"L→SUPR?"   (Ladder for suppression?)
"‼️3V-F4"   (URGENT: 3 victims Floor 4)
"AMB→F4"    (Ambulance to Floor 4)
"RTE-RDY"   (Route ready)
"F3✓2V"     (Floor 3 clear, 2 victims)
"GAS-HIGH"  (Gas pressure high)
```

#### **Transmission Limits**
- **Max per team**: 6 transmissions total
- **Cooldown**: 0.3 seconds between messages
- **Agent frequency**: Responds every 5 seconds
- **Radio interference**: Random 0.1-0.3s delays

#### **Message Types Detected**
- **Resource Request**: Contains "?" (e.g., "L→F4?")
- **Urgent Alert**: Contains "‼️" or "!" 
- **Coordination**: Contains "RTE", "EVAC", "CLEAR", "COORD"
- **Status Update**: General information sharing

### **⏰ Dynamic Crisis Events**

#### **Crisis Updates (Every 2 minutes)**
```
🚨FLASH#1: Fire spreading to east wing
🚨FLASH#2: Victim found on floor 3  
🚨FLASH#3: Gas pressure building
🚨FLASH#4: Structure collapse on floor 2
🚨FLASH#5: Ambulance arrival delayed
🚨FLASH#6: Evac route blocked by debris
```

#### **Deteriorating Conditions (Every 30 seconds)**
- **Gas Pressure**: Increases by 1 (max 10)
- **Building Stability**: Decreases by 1 (min 0)
- **Resource ETAs**: Count down automatically

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

### **🚀 Phase 1: Initial Response (0-30 seconds)**
1. **Game Initialization**: 
   - 3 AI agents spawn at starting locations
   - Crisis state established (fires, victims, blocked routes)
   - Resource allocation initialized (ladder with Fire team)

2. **Situation Assessment**:
   - Teams receive full crisis briefing
   - Each team evaluates priorities based on role
   - Initial communication begins

### **⚡ Phase 2: Active Coordination (30 seconds - 4 minutes)**
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

### **🏁 Phase 3: Final Push (4-5 minutes)**
1. **Escalating Urgency**:
   - Gas pressure near maximum (8-10/10)
   - Building stability critical (1-3/10)
   - Time pressure intensifies agent responses

2. **Last-Minute Coordination**:
   - Teams prioritize highest-impact actions
   - Resource sharing becomes more critical
   - Emergency vocabulary reaches peak development

### **📈 Real-Time Monitoring**

#### **Status Updates (Every minute)**
```
📊 STATUS UPDATE 📊
Time: 3:45 remaining
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
4. **8-Character Constraint**: Message parsed and validated
5. **Vocabulary Tracking**: New terms recorded for research

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

## 📄 License

This project is for research purposes. Please ensure compliance with Anthropic and Slack API terms of service. 