"""
LangGraph Agent với 5 nodes theo spec:
1. ParseNode - Phân tích, tách từng requirement
2. ConflictCheckNode - Phát hiện mâu thuẫn (contradiction/negation)
3. ClarityCheckNode - Phát hiện câu mơ hồ (ambiguous terms)
4. ImproveNode - Đề xuất rewrite rõ ràng hơn
5. AggregatorNode - Gom kết quả, format thành JSON
"""

import os
import json
from typing import TypedDict, List, Dict, Any
from pathlib import Path
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from app.utils.logger import logger

# Load environment variables
load_dotenv()

# Define Agent State
class AgentState(TypedDict):
    input_text: str
    parsed_requirements: List[str]
    conflicts: List[Dict[str, str]]
    ambiguities: List[Dict[str, str]]
    suggestions: List[Dict[str, str]]
    final_result: Dict[str, Any]


class RequirementsAnalysisAgent:
    """
    LangGraph Agent để phân tích SRS/User Stories
    Pipeline: ParseNode -> [ConflictCheckNode, ClarityCheckNode] (parallel) -> ImproveNode -> AggregatorNode
    """
    
    def __init__(self, api_key: str = None, model: str = "gemini-1.5-pro"):
        """
        Initialize the agent
        
        Args:
            api_key: Gemini API key (nếu None, lấy từ env GEMINI_API_KEY)
            model: Model name (gemini-1.5-pro hoặc gemini-1.5-flash)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Please set it in .env file")
        
        # Initialize LLM
        self.llm_pro = ChatGoogleGenerativeAI(
            google_api_key=self.api_key,
            model=model
        )
        
        # Use faster model for parallel checks
        self.llm_mini = ChatGoogleGenerativeAI(
            google_api_key=self.api_key,
            model="gemini-1.5-flash"  # Faster for parallel processing
        )
        
        # Load prompts
        self.prompts_dir = Path(__file__).parent / "prompts"
        self.parse_prompt = self._load_prompt("parse_requirements.txt")
        self.conflict_prompt = self._load_prompt("detect_conflict.txt")
        self.ambiguity_prompt = self._load_prompt("check_ambiguity.txt")
        self.improve_prompt = self._load_prompt("suggest_improve.txt")
        
        # Build graph
        self.graph = self._build_graph()
    
    def _load_prompt(self, filename: str) -> str:
        """Load prompt from file"""
        prompt_path = self.prompts_dir / filename
        if prompt_path.exists():
            return prompt_path.read_text(encoding='utf-8')
        else:
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    
    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow"""
        from langgraph.graph import END
        
        graph = StateGraph(AgentState)
        
        # Add nodes
        graph.add_node("parse_node", self.parse_node)
        graph.add_node("conflict_check_node", self.conflict_check_node)
        graph.add_node("clarity_check_node", self.clarity_check_node)
        graph.add_node("merge_results_node", self.merge_results_node)
        graph.add_node("improve_node", self.improve_node)
        graph.add_node("aggregator_node", self.aggregator_node)
        
        # Define flow
        graph.set_entry_point("parse_node")
        
        # Parse -> Parallel checks (both start from parse_node)
        graph.add_edge("parse_node", "conflict_check_node")
        graph.add_edge("parse_node", "clarity_check_node")
        
        # Parallel checks -> Merge (wait for both to complete)
        graph.add_edge("conflict_check_node", "merge_results_node")
        graph.add_edge("clarity_check_node", "merge_results_node")
        
        # Merge -> Improve
        graph.add_edge("merge_results_node", "improve_node")
        
        # Improve -> Aggregate
        graph.add_edge("improve_node", "aggregator_node")
        
        # Aggregate -> END
        graph.add_edge("aggregator_node", END)
        
        return graph.compile()
    
    def parse_node(self, state: AgentState) -> AgentState:
        """
        ParseNode: Phân tích văn bản, tách từng requirement
        Model: gemini-1.5-pro
        """
        logger.debug("Running ParseNode")
        prompt_template = PromptTemplate.from_template(self.parse_prompt)
        chain = prompt_template | self.llm_pro | StrOutputParser()
        
        result = chain.invoke({"input_text": state["input_text"]})
        
        # Parse requirements from result
        # Split by lines and clean
        requirements = []
        for line in result.split('\n'):
            line = line.strip()
            if line and len(line) > 5:  # Filter out very short lines
                # Remove markers like "-", "1.", "*", etc.
                line = line.lstrip('.-*0123456789) ').strip()
                if line:
                    requirements.append(line)
        
        logger.debug(f"Parsed {len(requirements)} requirements")
        return {
            "parsed_requirements": requirements
        }
    
    def conflict_check_node(self, state: AgentState) -> AgentState:
        """
        ConflictCheckNode: Phát hiện mâu thuẫn (contradiction/negation)
        Model: gemini-1.5-flash (mini)
        """
        logger.debug("Running ConflictCheckNode")
        if not state.get("parsed_requirements"):
            return {"conflicts": []}
        
        requirements_text = "\n".join([f"- {req}" for req in state["parsed_requirements"]])
        
        prompt_template = PromptTemplate.from_template(self.conflict_prompt)
        chain = prompt_template | self.llm_mini | StrOutputParser()
        
        result = chain.invoke({"parsed_requirements": requirements_text})
        
        # Parse JSON from result
        conflicts = self._parse_json_response(result, "conflicts")
        logger.debug(f"Found {len(conflicts)} conflicts")
        
        return {"conflicts": conflicts}
    
    def clarity_check_node(self, state: AgentState) -> AgentState:
        """
        ClarityCheckNode: Phát hiện câu mơ hồ (ambiguous terms)
        Model: gemini-1.5-flash (mini)
        """
        logger.debug("Running ClarityCheckNode")
        if not state.get("parsed_requirements"):
            return {"ambiguities": []}
        
        requirements_text = "\n".join([f"- {req}" for req in state["parsed_requirements"]])
        
        prompt_template = PromptTemplate.from_template(self.ambiguity_prompt)
        chain = prompt_template | self.llm_mini | StrOutputParser()
        
        result = chain.invoke({"parsed_requirements": requirements_text})
        
        # Parse JSON from result
        ambiguities = self._parse_json_response(result, "ambiguities")
        logger.debug(f"Found {len(ambiguities)} ambiguities")
        
        return {"ambiguities": ambiguities}
    
    def merge_results_node(self, state: AgentState) -> AgentState:
        """
        Merge node: Đợi cả conflict_check và clarity_check hoàn thành
        Đảm bảo cả conflicts và ambiguities đều có trong state
        """
        # Đảm bảo cả 2 keys đều có trong state
        merged_state = {
            "conflicts": state.get("conflicts", []),
            "ambiguities": state.get("ambiguities", []),
            "parsed_requirements": state.get("parsed_requirements", [])
        }
        return merged_state
    
    def improve_node(self, state: AgentState) -> AgentState:
        """
        ImproveNode: Đề xuất rewrite rõ ràng hơn
        Model: gemini-1.5-pro
        """
        logger.debug("Running ImproveNode")
        if not state.get("parsed_requirements"):
            return {"suggestions": []}
        
        requirements_text = "\n".join([f"- {req}" for req in state["parsed_requirements"]])
        
        conflicts_text = json.dumps(state.get("conflicts", []), indent=2, ensure_ascii=False)
        ambiguities_text = json.dumps(state.get("ambiguities", []), indent=2, ensure_ascii=False)
        
        prompt_template = PromptTemplate.from_template(self.improve_prompt)
        chain = prompt_template | self.llm_pro | StrOutputParser()
        
        result = chain.invoke({
            "parsed_requirements": requirements_text,
            "conflicts": conflicts_text,
            "ambiguities": ambiguities_text
        })
        
        # Parse JSON from result
        suggestions = self._parse_json_response(result, "suggestions")
        logger.debug(f"Generated {len(suggestions)} suggestions")
        
        return {"suggestions": suggestions}
    
    def aggregator_node(self, state: AgentState) -> AgentState:
        """
        AggregatorNode: Gom kết quả, format thành JSON
        Local function - không cần AI
        """
        final_result = {
            "conflicts": state.get("conflicts", []),
            "ambiguities": state.get("ambiguities", []),
            "suggestions": state.get("suggestions", [])
        }
        
        return {"final_result": final_result}
    
    def _parse_json_response(self, text: str, key: str = None) -> List[Dict]:
        """
        Parse JSON from LLM response
        Handles markdown code blocks and extracts JSON
        """
        # Remove markdown code blocks if present
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            text = text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            if end > start:
                text = text[start:end].strip()
        
        # Try to parse as JSON
        try:
            data = json.loads(text)
            if isinstance(data, dict) and key:
                return data.get(key, [])
            elif isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return list(data.values())[0] if len(data) == 1 else []
            else:
                return []
        except json.JSONDecodeError:
            # Try to extract JSON object using regex
            import re
            json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group())
                    if isinstance(data, dict) and key:
                        return data.get(key, [])
                    return data if isinstance(data, list) else []
                except:
                    pass
            
            # Fallback: return empty list
            return []
    
    def analyze(self, input_text: str) -> Dict[str, Any]:
        """
        Main method to analyze requirements
        
        Args:
            input_text: SRS/User Stories text to analyze
        
        Returns:
            Dict với keys: conflicts, ambiguities, suggestions
        """
        logger.info(f"Starting LangGraph analysis pipeline for text length: {len(input_text)} chars")
        initial_state: AgentState = {
            "input_text": input_text,
            "parsed_requirements": [],
            "conflicts": [],
            "ambiguities": [],
            "suggestions": [],
            "final_result": {}
        }
        
        # Run the graph
        try:
            final_state = self.graph.invoke(initial_state)
            logger.info("LangGraph pipeline completed successfully")
        except Exception as e:
            logger.error(f"LangGraph pipeline failed: {str(e)}")
            raise
        
        # Return final result
        result = final_state.get("final_result", {
            "conflicts": final_state.get("conflicts", []),
            "ambiguities": final_state.get("ambiguities", []),
            "suggestions": final_state.get("suggestions", [])
        })
        
        logger.info(f"Analysis result: {len(result.get('conflicts', []))} conflicts, "
                   f"{len(result.get('ambiguities', []))} ambiguities, "
                   f"{len(result.get('suggestions', []))} suggestions")
        
        return result

