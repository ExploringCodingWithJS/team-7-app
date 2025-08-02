import asyncio
import random
import time
from typing import Dict, List, Optional, Any, Tuple
from models import Tool, ToolResult, AgentConfig
from loguru import logger
from datetime import datetime

class ToolManager:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.tool_results: List[ToolResult] = []
        self.agent_tool_assignments: Dict[str, List[str]] = {}  # agent_id -> list of tool_ids
        self.tool_coordination_history: List[Dict] = []
        
        # Initialize available tools
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize the available tools for agents."""
        
        # Navigation and exploration tools
        self.tools["scanner"] = Tool(
            name="scanner",
            description="Scan surrounding area for structural integrity and hidden passages",
            parameters={"range": 3, "accuracy": 0.8},
            cooldown=2.0
        )
        
        self.tools["mapping_drone"] = Tool(
            name="mapping_drone",
            description="Deploy a small drone to explore inaccessible areas",
            parameters={"range": 5, "battery": 30},
            cooldown=10.0
        )
        
        self.tools["structural_analyzer"] = Tool(
            name="structural_analyzer",
            description="Analyze building stability and identify safe paths",
            parameters={"depth": 2, "precision": 0.9},
            cooldown=3.0
        )
        
        # Communication and coordination tools
        self.tools["signal_booster"] = Tool(
            name="signal_booster",
            description="Boost communication range and clarity between agents",
            parameters={"range": 4, "duration": 60},
            cooldown=15.0
        )
        
        self.tools["emergency_beacon"] = Tool(
            name="emergency_beacon",
            description="Create a beacon to guide other agents to your location",
            parameters={"visibility": 6, "duration": 120},
            cooldown=20.0
        )
        
        # Specialized tools
        self.tools["thermal_imager"] = Tool(
            name="thermal_imager",
            description="Detect heat signatures and identify potential exit locations",
            parameters={"range": 4, "sensitivity": 0.7},
            cooldown=5.0
        )
        
        self.tools["sonic_mapper"] = Tool(
            name="sonic_mapper",
            description="Use sound waves to map hidden passages and obstacles",
            parameters={"range": 3, "resolution": 0.8},
            cooldown=4.0
        )
        
        logger.info(f"Initialized {len(self.tools)} tools for agent use")
    
    def assign_tools_to_agents(self, agent_configs: List[AgentConfig]):
        """Assign tools to agents based on their roles and expertise."""
        
        # Role-based tool assignments
        role_tools = {
            "scout": ["scanner", "mapping_drone", "thermal_imager"],
            "navigator": ["structural_analyzer", "sonic_mapper", "scanner"],
            "coordinator": ["signal_booster", "emergency_beacon", "scanner"],
            "safety_officer": ["structural_analyzer", "thermal_imager", "emergency_beacon"],
            "communications_specialist": ["signal_booster", "emergency_beacon", "scanner"]
        }
        
        for agent_config in agent_configs:
            role = agent_config.role.value
            available_tools = role_tools.get(role, ["scanner"])  # Default to scanner
            
            # Assign 2-3 tools per agent
            num_tools = random.randint(2, min(3, len(available_tools)))
            assigned_tools = random.sample(available_tools, num_tools)
            
            # Set tool expertise levels
            for tool_name in assigned_tools:
                expertise = random.uniform(0.6, 1.0)  # Agents have varying expertise
                agent_config.tool_expertise[tool_name] = expertise
            
            agent_config.available_tools = assigned_tools
            self.agent_tool_assignments[agent_config.agent_id] = assigned_tools
            
            logger.info(f"Assigned tools to {agent_config.name}: {assigned_tools}")
    
    async def execute_tool(self, agent_id: str, tool_name: str, parameters: Dict[str, Any] = None) -> ToolResult:
        """Execute a tool and return the result."""
        
        if tool_name not in self.tools:
            return ToolResult(
                tool_id="",
                agent_id=agent_id,
                success=False,
                result={"error": f"Tool {tool_name} not found"}
            )
        
        tool = self.tools[tool_name]
        
        # Check if agent has access to this tool
        if tool_name not in self.agent_tool_assignments.get(agent_id, []):
            return ToolResult(
                tool_id=tool.tool_id,
                agent_id=agent_id,
                success=False,
                result={"error": f"Agent does not have access to {tool_name}"}
            )
        
        # Check cooldown
        if tool.last_used:
            time_since_use = (datetime.now() - tool.last_used).total_seconds()
            if time_since_use < tool.cooldown:
                return ToolResult(
                    tool_id=tool.tool_id,
                    agent_id=agent_id,
                    success=False,
                    result={"error": f"Tool {tool_name} is on cooldown ({tool.cooldown - time_since_use:.1f}s remaining)"}
                )
        
        # Simulate tool execution
        start_time = time.time()
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate execution time
        execution_time = time.time() - start_time
        
        # Generate tool-specific results
        result = await self._generate_tool_result(tool_name, parameters or {})
        
        # Update tool usage
        tool.last_used = datetime.now()
        tool.usage_count += 1
        
        # Create tool result
        tool_result = ToolResult(
            tool_id=tool.tool_id,
            agent_id=agent_id,
            success=result.get("success", True),
            result=result,
            execution_time=execution_time
        )
        
        self.tool_results.append(tool_result)
        logger.info(f"Tool {tool_name} executed by agent {agent_id}: {result.get('summary', 'Success')}")
        
        return tool_result
    
    async def _generate_tool_result(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate realistic results for each tool type."""
        
        if tool_name == "scanner":
            return {
                "success": True,
                "summary": "Area scan completed",
                "structural_integrity": random.uniform(0.3, 1.0),
                "hidden_passages": random.randint(0, 2),
                "threats_detected": random.randint(0, 1),
                "safe_paths": random.randint(1, 3)
            }
        
        elif tool_name == "mapping_drone":
            return {
                "success": True,
                "summary": "Drone exploration completed",
                "area_mapped": random.randint(3, 8),
                "new_paths_found": random.randint(1, 3),
                "battery_remaining": random.uniform(0.4, 0.9),
                "obstacles_identified": random.randint(0, 2)
            }
        
        elif tool_name == "structural_analyzer":
            return {
                "success": True,
                "summary": "Structural analysis complete",
                "stability_score": random.uniform(0.2, 1.0),
                "collapse_risk": random.uniform(0.0, 0.8),
                "safe_zones": random.randint(1, 4),
                "reinforcement_needed": random.randint(0, 2)
            }
        
        elif tool_name == "signal_booster":
            return {
                "success": True,
                "summary": "Communication enhanced",
                "signal_strength": random.uniform(0.6, 1.0),
                "range_boost": random.uniform(1.5, 3.0),
                "interference_reduced": random.uniform(0.3, 0.8),
                "duration_remaining": random.randint(30, 60)
            }
        
        elif tool_name == "emergency_beacon":
            return {
                "success": True,
                "summary": "Emergency beacon activated",
                "visibility_range": random.randint(4, 8),
                "duration_remaining": random.randint(60, 120),
                "agents_in_range": random.randint(0, 3),
                "signal_strength": random.uniform(0.7, 1.0)
            }
        
        elif tool_name == "thermal_imager":
            return {
                "success": True,
                "summary": "Thermal scan completed",
                "heat_signatures": random.randint(0, 3),
                "exit_probability": random.uniform(0.0, 0.9),
                "temperature_variations": random.randint(1, 4),
                "anomalies_detected": random.randint(0, 2)
            }
        
        elif tool_name == "sonic_mapper":
            return {
                "success": True,
                "summary": "Sonic mapping complete",
                "hidden_cavities": random.randint(0, 2),
                "passage_connections": random.randint(1, 4),
                "obstacle_details": random.randint(0, 3),
                "echo_patterns": random.randint(2, 6)
            }
        
        return {
            "success": False,
            "summary": "Unknown tool",
            "error": f"Tool {tool_name} not implemented"
        }
    
    def get_tool_coordination_opportunities(self, agent_positions: Dict[str, tuple]) -> List[Dict]:
        """Identify opportunities for coordinated tool use between nearby agents."""
        
        opportunities = []
        
        for agent1_id, pos1 in agent_positions.items():
            for agent2_id, pos2 in agent_positions.items():
                if agent1_id >= agent2_id:
                    continue
                
                # Calculate distance
                distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
                
                if distance <= 3:  # Agents within 3 cells
                    # Find complementary tools
                    tools1 = self.agent_tool_assignments.get(agent1_id, [])
                    tools2 = self.agent_tool_assignments.get(agent2_id, [])
                    
                    # Look for tool combinations that could be coordinated
                    coordination_ideas = self._find_tool_combinations(tools1, tools2)
                    
                    if coordination_ideas:
                        opportunities.append({
                            "agents": [agent1_id, agent2_id],
                            "distance": distance,
                            "coordination_ideas": coordination_ideas,
                            "priority": 1.0 / (distance + 1)  # Closer agents = higher priority
                        })
        
        return sorted(opportunities, key=lambda x: x["priority"], reverse=True)
    
    def _find_tool_combinations(self, tools1: List[str], tools2: List[str]) -> List[Dict]:
        """Find complementary tool combinations for coordination."""
        
        combinations = []
        
        # Scanner + Structural Analyzer = Comprehensive area analysis
        if "scanner" in tools1 and "structural_analyzer" in tools2:
            combinations.append({
                "tools": ["scanner", "structural_analyzer"],
                "description": "Comprehensive area analysis",
                "benefit": "Complete structural and threat assessment"
            })
        
        # Thermal Imager + Sonic Mapper = Hidden passage detection
        if "thermal_imager" in tools1 and "sonic_mapper" in tools2:
            combinations.append({
                "tools": ["thermal_imager", "sonic_mapper"],
                "description": "Hidden passage detection",
                "benefit": "Find concealed exits and passages"
            })
        
        # Signal Booster + Emergency Beacon = Team coordination
        if "signal_booster" in tools1 and "emergency_beacon" in tools2:
            combinations.append({
                "tools": ["signal_booster", "emergency_beacon"],
                "description": "Enhanced team coordination",
                "benefit": "Improved communication and team gathering"
            })
        
        # Mapping Drone + Scanner = Extended exploration
        if "mapping_drone" in tools1 and "scanner" in tools2:
            combinations.append({
                "tools": ["mapping_drone", "scanner"],
                "description": "Extended area exploration",
                "benefit": "Cover more ground with detailed analysis"
            })
        
        return combinations
    
    def record_tool_coordination(self, agents: List[str], tools: List[str], success: bool, result: Dict):
        """Record a tool coordination event."""
        
        coordination_event = {
            "timestamp": datetime.now(),
            "agents": agents,
            "tools": tools,
            "success": success,
            "result": result,
            "coordination_type": "synchronized_tool_use"
        }
        
        self.tool_coordination_history.append(coordination_event)
        logger.info(f"Tool coordination recorded: {agents} used {tools} - {'Success' if success else 'Failed'}")
    
    def get_tool_statistics(self) -> Dict[str, Any]:
        """Get statistics about tool usage and coordination."""
        
        total_uses = sum(tool.usage_count for tool in self.tools.values())
        coordination_events = len(self.tool_coordination_history)
        
        tool_usage = {}
        for tool_name, tool in self.tools.items():
            tool_usage[tool_name] = {
                "uses": tool.usage_count,
                "success_rate": tool.success_rate,
                "last_used": tool.last_used
            }
        
        return {
            "total_tool_uses": total_uses,
            "coordination_events": coordination_events,
            "tool_usage": tool_usage,
            "most_used_tool": max(self.tools.values(), key=lambda t: t.usage_count).name if self.tools else None
        } 