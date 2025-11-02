from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, List

class AgentState(TypedDict):
    input_text: str
    parsed_requirements: List[str]
    completeness_issues: List[str]
    enhancement_suggestions: List[str]

class RequirementsAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-1.5-flash")
        
        # Define the graph
        self.graph = self._build_graph()
    
    def _build_graph(self):
        graph = StateGraph(AgentState)
        
        # Add nodes
        graph.add_node("parse_requirements", self._parse_requirements)
        graph.add_node("analyze_completeness", self._analyze_completeness)
        graph.add_node("suggest_enhancements", self._suggest_enhancements)
        
        # Define edges
        graph.set_entry_point("parse_requirements")
        graph.add_edge("parse_requirements", "analyze_completeness")
        graph.add_edge("analyze_completeness", "suggest_enhancements")
        graph.add_edge("suggest_enhancements", END)
        
        return graph.compile()
    
    def _parse_requirements(self, state: AgentState):
        prompt = PromptTemplate.from_template(
            "Parse the following use case description into individual use case elements (actors, preconditions, main flow, alternative flows, postconditions, etc.):\n\n{input_text}\n\nOutput as a structured list."
        )
        chain = prompt | self.llm | StrOutputParser()
        parsed = chain.invoke({"input_text": state["input_text"]})
        requirements = [line.strip() for line in parsed.split('\n') if line.strip()]
        return {"parsed_requirements": requirements}
    
    def _analyze_completeness(self, state: AgentState):
        requirements = state["parsed_requirements"]
        prompt = PromptTemplate.from_template(
            "Analyze the following use case elements for completeness. Check for missing elements such as:\n- Clear actor identification\n- Preconditions\n- Main success scenario\n- Alternative flows\n- Exception handling\n- Postconditions\n- Non-functional requirements\n\nUse case elements:\n{requirements}\n\nList any missing or incomplete elements."
        )
        chain = prompt | self.llm | StrOutputParser()
        completeness_text = chain.invoke({"requirements": '\n'.join(requirements)})
        completeness_issues = [line.strip() for line in completeness_text.split('\n') if line.strip()]
        return {"completeness_issues": completeness_issues}
    
    def _suggest_enhancements(self, state: AgentState):
        requirements = state["parsed_requirements"]
        completeness_issues = state["completeness_issues"]
        prompt = PromptTemplate.from_template(
            "Based on the use case elements:\n{requirements}\n\nAnd completeness issues:\n{completeness_issues}\n\nProvide specific, actionable suggestions to improve the use case. Focus on:\n- Adding missing elements\n- Clarifying ambiguous parts\n- Improving structure\n- Enhancing usability\n- Adding error handling\n\nProvide suggestions as a numbered list for easy selection."
        )
        chain = prompt | self.llm | StrOutputParser()
        suggestions_text = chain.invoke({"requirements": '\n'.join(requirements), "completeness_issues": '\n'.join(completeness_issues)})
        enhancement_suggestions = [line.strip() for line in suggestions_text.split('\n') if line.strip()]
        return {"enhancement_suggestions": enhancement_suggestions}
    
    def analyze_and_get_state(self, input_text: str):
        initial_state = {
            "input_text": input_text,
            "parsed_requirements": [],
            "completeness_issues": [],
            "enhancement_suggestions": []
        }
        result = self.graph.invoke(initial_state)
        return result
    
    def select_suggestions(self, suggestions: List[str]):
        """
        Interactive method to let user select suggestions
        """
        print("\nAvailable Enhancement Suggestions:")
        for i, sug in enumerate(suggestions, 1):
            print(f"{i}. {sug}")
        
        selected = []
        while True:
            try:
                choice = input("\nEnter the number of suggestion to select (or 'done' to finish): ").strip()
                if choice.lower() == 'done':
                    break
                idx = int(choice) - 1
                if 0 <= idx < len(suggestions):
                    selected.append(suggestions[idx])
                    print(f"Selected: {suggestions[idx]}")
                else:
                    print("Invalid number. Try again.")
            except ValueError:
                print("Please enter a valid number or 'done'.")
        
        return selected