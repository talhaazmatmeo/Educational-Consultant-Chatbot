import json
import re
import requests
import os

# 🔹 Load Hugging Face API key (set in Streamlit Secrets or env)
HF_API_KEY = os.getenv("HF_API_KEY")  # ✅ use same key as app.py

# 🔹 Choose a lightweight free model
HF_MODEL = "google/gemma-2-2b-it"  # ✅ small + free-tier friendly

API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}


def query_huggingface(prompt: str) -> str:
    """Send prompt to Hugging Face Inference API."""
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 500}}

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)

        if response.status_code != 200:
            print("⚠️ HF API Error:", response.text)
            return ""

        result = response.json()

        # HF returns list of dicts with "generated_text"
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].strip()

        return str(result)

    except Exception as e:
        print("⚠️ Exception in Hugging Face call:", str(e))
        return ""


def extract_json(text: str):
    """Extract first JSON block from model output."""
    match = re.search(r"\{.*\}|\[.*\]", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None
    return None


def recommend_courses(degree: str, interest: str):
    """Recommend courses in JSON format using Hugging Face model."""
    prompt = f"""
    You are an educational consultant.
    Suggest 3 courses in JSON format only.
    Each course must include:
    - title
    - platform
    - skills (list)
    - duration
    - career_paths (list)

    Degree: {degree}
    Interest: {interest}
    """

    response = query_huggingface(prompt)
    courses = extract_json(response)
    return courses if courses else []


def degree_planner(degree: str):
    """Return recommended skills + career paths for a degree."""
    prompt = f"""
    You are an educational consultant.
    For the degree "{degree}", return JSON with:
    - recommended_skills (list)
    - possible_careers (list)
    """

    response = query_huggingface(prompt)
    planner = extract_json(response)
    return planner if planner else {}
