# Three-Team Emergency Response - Emergent Communication Study

## Team

### Team Number: 7

### Team Members (Names): Jeremy Samuel, Vedant Goenka

### Category Number: 3

## Game Design

### Title of Your Game:
**Emergency Fire Response - Emergent Communication Study**

### Describe the game:
A multi-agent system where **3 emergency response teams** (Fire 🔥, Medical 🚑, Police 👮) must coordinate during a major apartment building explosion crisis. Teams develop their own communication protocols under extreme constraints:

**Core Challenge:** 6 victims trapped across 4 floors with competing team priorities:
- **Fire Team**: Suppress fires → Rescue operations (owns heavy ladder)
- **Medical Team**: Immediate victim rescue → Hospital transport (needs ladder access)  
- **Police Team**: Evacuation control → Traffic management (controls routes)

**Critical Constraints:**
- **Communication**: Originally 8-character radio messages, now flexible length with unlimited transmissions
- **Resources**: 1 shared ladder, 2 ambulances, 1 evacuation route
- **Time Pressure**: 5-minute emergency scenario with escalating crisis events
- **Dynamic Events**: Gas pressure rises, building stability deteriorates, new fires/victims appear

**Success Condition:** Teams win by solving the complete emergency (all victims saved, fires contained, building stabilized, gas controlled) or the game ends after 5 minutes with performance scoring.

## Agent Design

### What makes this game a test of agentic behavior?

1. **Resource Negotiation**: Agents must negotiate shared resources (ladder, ambulances) without central coordination
2. **Dynamic Priority Management**: Teams balance competing objectives (fire suppression vs. victim rescue vs. evacuation)
3. **Emergent Communication**: Agents develop shorthand vocabulary and coordination protocols naturally
4. **Real-time Adaptation**: Agents respond to crisis events (gas pressure, structural collapse) and adjust strategies
5. **Multi-party Coordination**: Success requires 3+ agent coordination, not just pairwise interactions

### Did you design for any specific types of agents or capabilities?

**Agent Architecture**: Each team uses **Claude 3.5 Sonnet via Anthropic API** with specialized system prompts:

**Fire Team Agent:**
- Priority focus: Fire suppression → Structure safety → Victim rescue  
- Resources: Heavy rescue ladder, water supply
- Capabilities: Assess building stability, coordinate ladder deployment

**Medical Team Agent:**
- Priority focus: Victim rescue → Triage → Hospital transport
- Resources: Medical supplies
- Capabilities: Request ladder access, coordinate ambulances, assess victim conditions

**Police Team Agent:**
- Priority focus: Evacuation control → Traffic management → Route clearing
- Resources: None (coordination role)
- Capabilities: Manage evacuation routes, coordinate ambulance access, crowd control

**Key Agent Capabilities Required:**
- **Situational Awareness**: Process crisis state, resource allocation, team statuses
- **Strategic Planning**: Balance immediate needs vs. long-term objectives
- **Communication Protocol Development**: Create efficient emergency vocabulary
- **Resource Competition**: Negotiate fairly while pursuing team objectives

### How does success or failure reflect the agent's performance?

**Primary Success Metrics:**
1. **Problem Solving**: Complete emergency resolution (all victims saved, fires contained, building stable, gas controlled)
2. **Coordination Events**: Successful resource sharing and joint operations
3. **Communication Efficiency**: Vocabulary development and message effectiveness
4. **Time Performance**: Speed of coordination and crisis resolution

**Performance Indicators:**
- **Coordination Success Rate**: Percentage of successful resource negotiations
- **Emergent Vocabulary Complexity**: Shorthand terms, coordination phrases, urgency signals developed
- **Response Adaptability**: How quickly agents adjust to crisis events
- **Resource Utilization**: Efficiency of ladder/ambulance deployment

**Failure Modes:**
- **Communication Breakdown**: Teams talk past each other, no vocabulary convergence
- **Resource Deadlock**: Teams compete destructively for shared resources
- **Priority Misalignment**: Teams pursue conflicting objectives without compromise
- **Crisis Escalation**: Agents fail to respond to deteriorating conditions

## Evaluation

### Emergent Language: Did the language exhibit surprising depth? Did these properties emerge naturally, without being explicitly instructed?

**Yes, the system demonstrates natural language emergence:**

**Vocabulary Development Tracking:**
- **Shorthand Creation**: Agents develop location codes (F1-F4, EW, WW), resource abbreviations (L→, AMB→)
- **Urgency Signaling**: Natural adoption of "‼️" prefix and exclamation patterns for critical situations
- **Coordination Protocols**: Teams create action sequences ("L→F4-1MIN", "AMB→F4-GO") without explicit instruction

**Emergent Properties:**
- **Context-Dependent Meaning**: Same symbols mean different things to different teams
- **Protocol Evolution**: Communication patterns become more sophisticated over multiple games
- **Negotiation Language**: Teams develop implicit bargaining vocabulary ("?", "✓", "→")

**Natural Emergence Mechanisms:**
- **Constraint-Driven Innovation**: Character limits force creative abbreviation
- **Feedback Loops**: Successful communications get repeated and refined
- **Inter-team Adaptation**: Teams converge on mutually understood protocols

### Task Completion: How successfully and efficiently did the agents complete the game objectives?

**Success Measurement System:**
- **Complete Success**: All victims saved + fires contained + building stable + gas controlled
- **Partial Success**: Scoring based on lives saved (100pt), fires contained (50pt), evacuations (25pt)
- **Coordination Bonus**: Points for successful resource sharing events
- **Efficiency Metrics**: Time to coordination, resource utilization rates

**Typical Performance Patterns:**
- **Early Game**: High message volume, resource conflicts, vocabulary experimentation
- **Mid Game**: Protocol stabilization, successful coordinations increase
- **Late Game**: Refined communication, focus on remaining objectives

**Success Factors:**
- **Resource Negotiation Speed**: Teams that establish ladder-sharing protocols early perform better
- **Crisis Responsiveness**: Teams that adapt quickly to gas/stability alerts maintain higher scores
- **Communication Convergence**: Games with faster vocabulary alignment show better coordination

### Domain Realism: Does your game represent a realistic coordination challenge? Why or why not?

**High Domain Realism:**

**Authentic Emergency Response Elements:**
- **Resource Scarcity**: Real emergencies have limited ladders, ambulances, personnel
- **Competing Priorities**: Fire suppression vs. rescue vs. evacuation conflicts occur in real incidents
- **Communication Constraints**: Radio bandwidth limitations and emergency protocols are realistic
- **Time Pressure**: Emergency response windows are genuinely critical
- **Dynamic Conditions**: Real emergencies involve escalating secondary hazards

**Realistic Coordination Challenges:**
- **Multi-agency Coordination**: Fire/Medical/Police coordination mirrors real emergency response
- **Incident Command Structure**: Resource allocation and priority conflicts reflect real systems
- **Communication Protocol Evolution**: Emergency services do develop specialized vocabularies

**Research Validation:**
- **Emergency Management Literature**: Game mechanics align with documented coordination challenges
- **Real Incident Analysis**: Resource conflicts and communication breakdowns are common failure modes
- **Training Scenarios**: Similar to tabletop exercises used in emergency management training

**Limitations:**
- **Simplified Geography**: Real buildings have more complex layouts
- **Reduced Personnel**: Real teams have more complex internal coordination
- **Streamlined Resources**: Real emergencies involve more equipment types

## Additional Questions

### If you had more time, how would you improve or enhance this game?

**1. Enhanced Realism:**
- **Complex Building Models**: Multi-story layouts with stairs, elevators, ventilation systems
- **Weather Conditions**: Wind affecting fire spread, rain impacting visibility/safety
- **Civilian Behavior**: Non-agent civilians who panic, help, or hinder operations
- **Equipment Failures**: Random resource breakdowns requiring adaptation

**2. Advanced Agent Capabilities:**
- **Multi-LLM Comparison**: Test different models (GPT-4, Claude, Llama) for communication differences
- **Human-AI Mixed Teams**: Allow human players to join as team members
- **Hierarchical Agents**: Incident commanders who coordinate between teams
- **Learning Agents**: Teams that improve coordination over multiple games

**3. Communication Research:**
- **Linguistic Analysis**: Track grammar evolution, semantic drift, protocol convergence
- **Cross-Cultural Communication**: Teams with different "cultural" starting vocabularies
- **Information Asymmetry**: Teams with different knowledge about the crisis
- **Communication Channels**: Separate public/private channels for strategy

**4. Scenario Complexity:**
- **Multiple Crisis Types**: Chemical spills, earthquakes, terrorist attacks
- **Building Variations**: Hospitals, schools, high-rises with different challenges
- **Multi-Incident Scenarios**: Teams handling multiple simultaneous emergencies
- **Long-term Campaigns**: Teams that build relationships over multiple incidents

**5. Evaluation & Analytics:**
- **Real Emergency Responder Validation**: Have actual fire/medical/police personnel evaluate realism
- **Communication Network Analysis**: Graph theory analysis of information flow
- **Performance Prediction**: ML models that predict coordination success from early messages
- **Vocabulary Convergence Studies**: Measure how quickly teams develop shared languages

**6. Research Applications:**
- **Emergency Management Training**: Use as training tool for real response teams
- **Organization Design**: Study optimal team structures for coordination
- **AI Safety Research**: Test alignment and cooperation in high-stakes scenarios
- **Disaster Response Optimization**: Inform real emergency response protocol development

---

## Quick Start Guide

### Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Copy `env_example.txt` to `.env` and fill in your API keys:
   ```
   ANTHROPIC_API_KEY=your_anthropic_key_here
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_APP_TOKEN=xapp-your-app-token
   SLACK_CHANNEL_ID=C1234567890
   ```
3. Configure Slack app with Socket Mode and required permissions
4. Run: `python main.py`
5. Type `<START_GAME>` in your Slack channel

### Game Commands
- `<START_GAME>` - Start emergency response mission
- `/agent status` - Show current game status  
- `/agent stop` - Stop current game
- `QUIT_GAME` - End game with analysis

### Research Features
- **Real-time Communication Analysis**: Tracks vocabulary development during games
- **Coordination Success Metrics**: Measures resource sharing effectiveness
- **Emergent Language Detection**: Identifies shorthand and protocol development
- **Performance Analytics**: Exports detailed game data for research analysis