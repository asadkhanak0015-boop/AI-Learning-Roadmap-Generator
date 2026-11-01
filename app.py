import os

import streamlit as st
from groq import Groq

# ---------- Page config ----------
st.set_page_config(
    page_title="AI Learning Roadmap Generator",
    page_icon="🗺️",
    layout="centered",
)

DEFAULT_MODEL = "llama-3.3-70b-versatile"
MODEL_OPTIONS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "openai/gpt-oss-20b",
]
LEVELS = ["Beginner", "Intermediate", "Advanced"]
TIME_UNITS = ["Weeks", "Months"]


# ---------- Helpers ----------
def get_api_key() -> str | None:
    """Read the Groq API key from Streamlit secrets or environment variables."""
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY")


def build_prompt(field: str, level: str, duration: int, unit: str, hours_per_week: int) -> str:
    return f"""Create a detailed, practical learning roadmap.

Field / Topic: {field}
Current level: {level}
Total time available: {duration} {unit.lower()}
Study time per week: {hours_per_week} hours

Structure the answer in Markdown with these sections:

## 🎯 Overview
Short summary of what the learner will achieve and the domain/area this field belongs to.

## 🧱 Prerequisites
What to know before starting (say "None" if nothing is needed).

## 📅 Roadmap
Break the total time into {unit.lower()[:-1]}-by-{unit.lower()[:-1]} (or phase-by-phase if that is more sensible) steps.
For each step include: goal, key topics, and estimated hours.

## 🛠️ Projects
3-5 hands-on projects that match the level, from small to capstone.

## 📚 Recommended Resources
Free and well-known courses, books, documentation, and communities. Do not invent URLs; name the resources only.

## ✅ Milestones & Self-Check
How the learner can measure progress along the way.

## 💡 Tips
Short practical advice for staying consistent.

Be realistic about what can be learned in the given time. Tailor depth to the {level} level."""


def generate_roadmap(api_key: str, model: str, prompt: str, temperature: float):
    """Stream the roadmap from Groq."""
    client = Groq(api_key=api_key)
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert learning coach and curriculum designer. "
                    "You create clear, realistic, well-structured learning roadmaps."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=4096,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = get_api_key()
    if not api_key:
        api_key = st.text_input("Groq API Key", type="password", help="Get one free at console.groq.com")
    else:
        st.success("API key loaded")

    model = st.selectbox("Model", MODEL_OPTIONS, index=MODEL_OPTIONS.index(DEFAULT_MODEL))
    temperature = st.slider("Creativity", 0.0, 1.0, 0.5, 0.1)
    st.caption("Powered by Groq + Streamlit")

# ---------- Main UI ----------
st.title("🗺️ AI Learning Roadmap Generator")
st.write("Tell me what you want to learn, your level, and how much time you have. I'll build your roadmap.")

field = st.text_input("What do you want to learn?", placeholder="e.g. Machine Learning, Web Development, Cybersecurity")

col1, col2 = st.columns(2)
with col1:
    level = st.selectbox("Your level", LEVELS)
with col2:
    hours_per_week = st.number_input("Hours per week", min_value=1, max_value=80, value=10, step=1)

col3, col4 = st.columns(2)
with col3:
    duration = st.number_input("Time to learn", min_value=1, max_value=60, value=3, step=1)
with col4:
    unit = st.selectbox("Unit", TIME_UNITS, index=1)

if st.button("🚀 Generate Roadmap", type="primary", use_container_width=True):
    if not field.strip():
        st.warning("Please enter a field or topic.")
    elif not api_key:
        st.error("Please provide a Groq API key in the sidebar or in Streamlit secrets.")
    else:
        prompt = build_prompt(field.strip(), level, int(duration), unit, int(hours_per_week))
        try:
            with st.spinner("Building your roadmap..."):
                placeholder = st.empty()
                text = ""
                for piece in generate_roadmap(api_key, model, prompt, temperature):
                    text += piece
                    placeholder.markdown(text)
            st.session_state["roadmap"] = text
            st.session_state["roadmap_name"] = field.strip().replace(" ", "_")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

if st.session_state.get("roadmap"):
    st.download_button(
        "⬇️ Download roadmap (.md)",
        data=st.session_state["roadmap"],
        file_name=f"{st.session_state['roadmap_name']}_roadmap.md",
        mime="text/markdown",
    )
