from backend.app.agent import RequirementsAgent
from dotenv import load_dotenv
import os

# load dotenv from backend/.env so config lives with backend
load_dotenv('backend/.env')

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Please set GOOGLE_API_KEY in .env file")
        return

    agent = RequirementsAgent(api_key)
    
    print("Use Case Analysis Tool")
    print("======================")
    
    # Get use case input from user
    print("Enter your use case description (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    input_text = "\n".join(lines)
    
    if not input_text.strip():
        print("No input provided. Exiting.")
        return
    
    print("\nAnalyzing use case...")
    result = agent.analyze(input_text)
    print(result)
    
    # For interactive selection, we need to modify agent to return state
    # Let's add a method to get the analysis state
    analysis_state = agent.analyze_and_get_state(input_text)
    
    if analysis_state["enhancement_suggestions"]:
        print("\nWould you like to select suggestions to implement? (y/n)")
        choice = input().strip().lower()
        if choice == 'y':
            selected = agent.select_suggestions(analysis_state["enhancement_suggestions"])
            print("\nSelected suggestions:")
            for sel in selected:
                print(f"- {sel}")
    else:
        print("\nNo suggestions available.")

if __name__ == "__main__":
    main()