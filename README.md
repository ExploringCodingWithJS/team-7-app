# 🚨 Three-Team Emergency Response - Emergent Communication Study

A multi-agent system where **3 emergency response teams** must coordinate during a crisis scenario using **8-character emergency radio protocol**. The goal is to observe how agents spontaneously develop their own language and coordination patterns under extreme time pressure.

## 🎯 Core Concept

**Three emergency response teams** must coordinate during a major apartment building explosion:

- **🔥 Fire Team**: Rescue equipment, fire suppression, hazmat gear
- **🚑 Medical Team**: Paramedics, ambulances, medical supplies, trauma equipment  
- **👮 Police Team**: Evacuation support, traffic control, crowd barriers, investigation units

## 🎮 Game Mechanics

### **Competing Priorities**
- **Fire Team**: Wants to suppress fire first, then rescue
- **Medical Team**: Needs immediate victim access, wants Fire to prioritize rescue
- **Police Team**: Must evacuate surrounding buildings, needs Medical to triage so ambulances can move

### **Critical Resource Constraints**
- Only **1 heavy rescue ladder** available
- Only **2 ambulances** on scene  
- Only **1 safe evacuation route** (others blocked by debris)

### **Communication Pressure**
- **8-character message limit** (emergency radio protocol)
- **6 transmissions max** per team
- **Random 0.3s delays** (radio interference from the fire)

### **Dynamic Crisis**
Every 2 minutes: `🚨FLASH#N` - situation changes
- "Fire spreading to east wing"
- "Victim found on floor 3"
- "Gas pressure building"

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

## 📊 Game Flow

1. **Initialization**: 3 teams deployed to crisis scene
2. **Resource Assessment**: Teams discover limited resources available
3. **Coordination Phase**: Teams negotiate for shared resources
4. **Crisis Events**: Dynamic events change priorities every 2 minutes
5. **Final Scoring**: Lives saved, fire contained, people evacuated

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

## 📄 License

This project is for research purposes. Please ensure compliance with Anthropic and Slack API terms of service. 