# 🗺️ AI Learning Roadmap Generator

A Streamlit app that creates a personalized learning roadmap using the Groq API.
Enter a field, your level (Beginner / Intermediate / Advanced), and the time you have, and get a structured plan with phases, projects, resources, and milestones.

## Features
- Field/topic, level, duration (weeks or months), and weekly hours as inputs
- Streaming responses from Groq LLMs
- Choice of model and creativity level
- Download the roadmap as a Markdown file

## Run locally
```bash
pip install -r requirements.txt
export GROQ_API_KEY="your_key_here"   # Windows: set GROQ_API_KEY=your_key_here
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app from the repo (main file: `app.py`).
3. Under **Advanced settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
4. Deploy.

Get a free API key at [console.groq.com](https://console.groq.com).

## Project structure
```
.
├── app.py
├── requirements.txt
└── README.md
```

## Notes
Groq retires models from time to time. If a model errors out, update `MODEL_OPTIONS` in `app.py` with a currently available one from the Groq console.
