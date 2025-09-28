import json
import time
import sys
import signal
from utils import save_json, load_json
from recommender import recommend_courses, degree_planner

SESSION_FILE = "sessions.json"

# Handle Ctrl+C gracefully
def handle_exit(sig, frame):
    print("\n🛑 Chat stopped by user.\n")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

def stream_print(text, delay=0.03):
    """Print text like typing effect, one char at a time."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def start_chat():
    stream_print("\n🤖 Hello! I’m your Edu Consultant Chatbot.")
    stream_print("I’ll guide you with courses and career advice.\n")

    # Ask user details
    name = input("👤 What is your name? (or 'q' to quit): ")
    if name.lower() == "q":
        return
    degree = input("🎓 What degree are you pursuing (or completed)? ")
    interest = input("💡 What is your main interest area? (e.g., AI, Web Dev, Cybersecurity) ")

    stream_print(f"\n✅ Thanks {name}! I’ve saved your profile.")
    stream_print("\n🤔 Analyzing your degree, skills, and interests...\n")
    time.sleep(2)

    # --- Course Recommendations ---
    recommendations = recommend_courses(degree, interest)

    all_course_skills = []
    recommended_titles = []

    stream_print("📚 Based on your degree and interest, here are some recommended courses:\n")
    if recommendations:
        for idx, course in enumerate(recommendations, 1):
            stream_print(f"{idx}. {course['title']} ({course['platform']})")
            stream_print(f"   Skills: {', '.join(course['skills'])}")
            stream_print(f"   Duration: {course['duration']}")
            stream_print(f"   Career Paths: {', '.join(course['career_paths'])}\n")
            all_course_skills.extend(course["skills"])
            recommended_titles.append(course["title"])
    else:
        stream_print("😕 Sorry, I couldn’t find any matching courses. Try another interest.")

    # --- Degree Planner ---
    stream_print("\n🤔 Preparing your degree career planner...")
    time.sleep(2)

    degree_info = degree_planner(degree)
    skill_gap = []
    if degree_info:
        stream_print("\n🎯 Career Paths you can target with your degree:")
        for career in degree_info["careers"]:
            stream_print(f"   - {career}")

        stream_print("\n🛠 Recommended skills for your degree:")
        stream_print(", ".join(degree_info["recommended_skills"]))

        if all_course_skills:
            missing_skills = set(degree_info["recommended_skills"]) - set(all_course_skills)
            if missing_skills:
                stream_print("\n⚡ Skill Gap detected! You still need to learn:")
                stream_print(", ".join(missing_skills))
                skill_gap = list(missing_skills)
            else:
                stream_print("\n✅ Great! Recommended courses already cover your key skills.")
    else:
        stream_print("\nℹ️ No detailed planner available for your degree.")

    # Save session
    session = {
        "name": name,
        "degree": degree,
        "interest": interest,
        "recommended_courses": recommended_titles,
        "skill_gap": skill_gap
    }

    sessions = load_json(SESSION_FILE)
    if not isinstance(sessions, list):
        sessions = []
    sessions.append(session)
    save_json(SESSION_FILE, sessions)


def show_saved_sessions():
    sessions = load_json(SESSION_FILE)
    if not sessions or not isinstance(sessions, list):
        print("📂 No saved sessions found.")
        return

    stream_print("\n📂 Saved Sessions:\n")
    for idx, s in enumerate(sessions, 1):
        stream_print(f"{idx}. {s['name']} | Degree: {s['degree']} | Interest: {s['interest']}")
        if s.get("recommended_courses"):
            stream_print(f"   Courses: {', '.join(s['recommended_courses'])}")
        if s.get("skill_gap"):
            stream_print(f"   Skill Gap: {', '.join(s['skill_gap'])}")
        print()
