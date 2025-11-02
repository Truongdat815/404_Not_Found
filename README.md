<<<<<<< HEAD
# Requirements Engineering AI Agent

This application uses LangGraph to build an AI agent that analyzes Software Requirements Specifications (SRS) and User Stories, detects conflicts, and suggests improvements.

## Features

- **Parse Requirements**: Extracts individual requirements from SRS/User Stories text.
- **Conflict Detection**: Identifies inconsistencies or conflicts between requirements.
- **Improvement Suggestions**: Provides recommendations to resolve conflicts and enhance requirements.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - Edit `.env` file and add your Google Gemini API key:
     ```
     GOOGLE_API_KEY=your_actual_gemini_api_key_here
     ```

## Usage

Run the main script:
```bash
python main.py
```

The agent will analyze a sample input and output the parsed requirements, detected conflicts, and suggestions.

## Architecture

The agent is built using LangGraph with the following workflow:

1. **Parse Requirements Node**: Uses Gemini 1.5 Flash to parse input text into individual requirements.
2. **Detect Conflicts Node**: Analyzes requirements for conflicts and inconsistencies.
3. **Suggest Improvements Node**: Generates suggestions to resolve conflicts and improve requirements.

The state is managed through a TypedDict with keys: `input_text`, `parsed_requirements`, `conflicts`, `suggestions`.

## Customization

- Modify the prompts in `agent.py` to customize the analysis behavior.
- Add more nodes or edges to the graph for additional functionality.
- Integrate with other LLMs or add more advanced NLP processing.
=======
#  404_Not_Found – AI Agent for SDLC Hackathon

##  Team Members

| No. | Student ID | Full Name | Role |
|:---:|:-----------:|:----------------------------|:---------------------------|
| 1 | SE192964 | Ngô Hoàng Trường Đạt |  Team Leader |
| 2 | SE192637 | Phạm Vũ Hoài Phương Thảo |  Backend Developer |
| 3 | SE194805 | Phạm Trần Đăng Phú |  Frontend Developer |

---

##  Team Overview

We are **404_Not_Found**, a passionate team of three FPT University students participating in the **AI Agent for SDLC Hackathon**, competing under **Track 1 – Topic 2: Requirements Engineering App**.

Our mission is to build an **AI-powered Requirements Engineering Assistant** that helps software teams refine and validate requirements efficiently.  
Using advanced natural language understanding and reasoning, our app automatically analyzes **Software Requirement Specifications (SRS)** and **User Stories** to detect **conflicts, ambiguities**, and provide **improvement suggestions** — ensuring greater clarity, consistency, and alignment throughout the software development lifecycle.

---

##  Vision

Empowering developers with smarter requirement validation through AI — reducing misunderstandings, improving collaboration, and accelerating high-quality software delivery.

---

##  Tech Stack

- **Core AI:** OpenAI, Claude, ChatGPT, Cursor
- **Frontend:** React / Vite / TailwindCSS  
- **Backend:** Node.js / FastAPI  
- **Database:** SQL Server  

---

 *Built with passion and precision by 404_Not_Found – FPT University.*

>>>>>>> upstream/thaobackend
