# Clinic Notes Backend
FastAPI backend for a medical research chatbot with live web search. Built with LangChain, Groq and DuckDuckGo.

## Run
1. Copy .env.example to .env and add your Groq key.
2. Install the dependencies from pyproject.toml.
3. Run: `uvicorn app.main:app --reload`
4. API docs: `http://localhost:8000/api/docs`

# Clinic Notes Frontend

Chat interface for a medical research chatbot with live web search. Built with plain HTML, CSS and JavaScript.

## Features

- Light and dark themes
- Responsive layout for desktop and mobile
- Formatted answers with headings, lists and tables
- Suggested questions, copy button and character counter
- Clear error messages when the backend is unreachable

## Run

1. Start the backend on http://localhost:8000
2. In this folder, run: `python -m http.server 3000`
3. Open http://localhost:3000

The backend URL is set at the top of the script in `index.html`:

```js
const API_URL = "http://localhost:8000/api/v1/chat";
```

## Demo.mp4

<video src="Demo.mp4" width="320" height="240" controls></video>

## Disclaimer

General information only. Not medical advice.

