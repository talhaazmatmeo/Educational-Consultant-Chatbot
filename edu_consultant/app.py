import streamlit as st
import time
import requests
import os
from utils import save_json, load_json
from recommender import recommend_courses, degree_planner

SESSION_FILE = "sessions.json"

# 🔹 Hugging Face API setup
HF_API_KEY = os.getenv("HF_API_KEY")  # put your key in Streamlit Secrets
HF_MODEL = "google/gemma-2-2b-it"     # free small model

def ask_huggingface(prompt):
    """Send a prompt to Hugging Face Inference API."""
    try:
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json={"inputs": prompt},
            timeout=60,
        )
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"].strip()
            return str(data)
        else:
            return f"⚠️ API Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"⚠️ Error calling Hugging Face: {str(e)}"


# 🔹 Chatbot UI
def chatbot_ui():
    st.header("💬 Chat with Edu Consultant Bot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("🧑 You:", "")
    if st.button("Send") and user_input.strip():
        st.session_state.chat_history.append(("🧑", user_input))

        with st.spinner("🤖 Thinking..."):
            bot_response = ask_huggingface(user_input)
        st.session_state.chat_history.append(("🤖", bot_response))

    for speaker, text in st.session_state.chat_history:
        st.markdown(f"**{speaker}:** {text}")


# 🔹 Consultant UI
def consultant_ui():
    st.header("🎓 Edu Consultant – Courses & Career Planner")

    name = st.text_input("👤 What is your name?")
    degree = st.text_input("🎓 Degree you are pursuing (or completed)?")
    interest = st.text_input("💡 Your main interest area (e.g., AI, Web Dev, Cybersecurity)")

    if st.button("🔍 Get Recommendations"):
        if not name or not degree or not interest:
            st.warning("⚠️ Please fill in all fields.")
            return

        st.success(f"✅ Thanks {name}! Let’s analyze your profile...")
        time.sleep(1)

        # 🔹 Course recommendations
        st.subheader("📚 Recommended Courses")
        recommendations = recommend_courses(degree, interest)
        all_course_skills = []
        recommended_titles = []

        if recommendations:
            for idx, course in enumerate(recommendations, 1):
                st.markdown(f"**{idx}. {course['title']} ({course['platform']})**")
                st.markdown(f"   - 🛠 Skills: {', '.join(course['skills'])}")
                st.markdown(f"   - ⏳ Duration: {course['duration']}")
                st.markdown(f"   - 🎯 Career Paths: {', '.join(course['career_paths'])}")
                all_course_skills.extend(course["skills"])
                recommended_titles.append(course["title"])
        else:
            st.info("😕 Sorry, I couldn’t find any matching courses. Try another interest.")

        # 🔹 Degree planner
        st.subheader("🗂 Degree Career Planner")
        degree_info = degree_planner(degree)
        skill_gap = []

        if degree_info:
            st.markdown("**🎯 Career Paths:**")
            for career in degree_info.get("possible_careers", []):
                st.markdown(f"- {career}")

            st.markdown("**🛠 Recommended Skills:**")
            st.write(", ".join(degree_info.get("recommended_skills", [])))

            if all_course_skills:
                missing_skills = set(degree_info.get("recommended_skills", [])) - set(all_course_skills)
                if missing_skills:
                    st.warning("⚡ Skill Gap detected!")
                    st.write(", ".join(missing_skills))
                    skill_gap = list(missing_skills)
                else:
                    st.success("✅ Great! Recommended courses already cover your key skills.")
        else:
            st.info("ℹ️ No detailed planner available for your degree.")

        # 🔹 Save session
        session = {
            "name": name,
            "degree": degree,
            "interest": interest,
            "recommended_courses": recommended_titles,
            "skill_gap": skill_gap,
        }
        sessions = load_json(SESSION_FILE)
        if not isinstance(sessions, list):
            sessions = []
        sessions.append(session)
        save_json(SESSION_FILE, sessions)
        st.success("💾 Session saved!")


# 🔹 Saved Sessions UI
def saved_sessions_ui():
    st.header("📂 Saved Sessions")
    sessions = load_json(SESSION_FILE)

    if not sessions or not isinstance(sessions, list):
        st.info("📂 No saved sessions found.")
        return

    for idx, s in enumerate(sessions, 1):
        st.markdown(f"**{idx}. {s['name']} | Degree: {s['degree']} | Interest: {s['interest']}**")
        if s.get("recommended_courses"):
            st.markdown(f"- 📚 Courses: {', '.join(s['recommended_courses'])}")
        if s.get("skill_gap"):
            st.markdown(f"- ⚡ Skill Gap: {', '.join(s['skill_gap'])}")
        st.markdown("---")


# 🔹 Main
def main():
    st.title("🎓 Edu Consultant Chatbot")
    tabs = st.tabs(["💬 Chatbot", "🎓 Consultant", "📂 Saved Sessions"])

    with tabs[0]:
        chatbot_ui()
    with tabs[1]:
        consultant_ui()
    with tabs[2]:
        saved_sessions_ui()


if __name__ == "__main__":
    main()
