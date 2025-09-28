from chatbot import start_chat, show_saved_sessions
from utils import load_json

def main():
    print("🎓 Welcome to Edu Consultant Chatbot!")

    # Load data once at startup
    courses = load_json("data/courses.json")
    degrees = load_json("data/degrees.json")

    if courses and degrees:
        print(f"✅ Loaded {len(courses)} courses and {len(degrees)} degrees from database.\n")
    else:
        print("⚠️ Warning: Could not load courses or degrees properly.\n")

    while True:
        print("\nChoose an option:")
        print("1. Start new chat")
        print("2. View saved sessions")
        print("3. Exit")

        choice = input("👉 Enter your choice (1/2/3): ")

        if choice == "1":
            start_chat()
        elif choice == "2":
            show_saved_sessions()
        elif choice == "3":
            print("👋 Goodbye! See you next time.")
            break
        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    main()
