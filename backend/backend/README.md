# Backend - AI Requirements Engineering API

## Tech Stack
- FastAPI
- LangGraph
- OpenAI GPT-4o / Claude 3 Sonnet
- LlamaIndex
- SQLite

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

## API Endpoints

- `POST /analyze` - Analyze SRS/User Stories

## Project Structure

```
backend/
├── main.py                 # Entry point FastAPI
├── requirements.txt        # Python dependencies
├── app/
│   ├── api/
│   │   ├── router.py      # API endpoints
│   │   └── schema.py      # Pydantic models
│   ├── services/
│   │   ├── analyzer.py    # AI analysis logic
│   │   ├── parser.py      # Text parsing
│   │   └── formatter.py   # Output formatting
│   ├── agents/
│   │   ├── langgraph_agent.py
│   │   └── prompts/
│   └── utils/
└── tests/
```

