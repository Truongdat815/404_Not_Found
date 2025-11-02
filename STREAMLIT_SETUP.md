# Streamlit Setup Guide

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python -m streamlit run app.py
```

Hoặc nếu `streamlit` đã có trong PATH:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
.
├── app.py                      # Main Streamlit application
├── pages/
│   └── 1_Analyze_Document.py   # Document analysis page
├── core/
│   └── agent.py                # Agent module (app.invoke())
├── requirements.txt            # Python dependencies
└── backend/                    # Backend API (if needed)
```

## Usage

1. Open the app in your browser
2. Navigate to "Analyze Document" page
3. Upload a .txt file or paste your SRS/User Stories text
4. Click "Analyze Document"
5. View results in tabs: Conflicts, Ambiguities, Suggestions
6. Export results as JSON or Text

## Notes

- The `core/agent.py` currently contains a mock implementation
- Replace the `app.invoke()` method with your actual LangGraph agent implementation
- The frontend is now fully built with Streamlit (React has been removed)

