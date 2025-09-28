from recommender import recommend_courses, degree_planner
import json

print("🔍 Testing course recommendations...\n")

degree = "BS Computer Science"
interest = "Artificial Intelligence"

courses = recommend_courses(degree, interest)
print("📚 Recommended Courses:")
print(json.dumps(courses, indent=2, ensure_ascii=False))  # ✅ Pretty print JSON

print("\n🔍 Testing degree planner...\n")

planner = degree_planner(degree)
print(json.dumps(planner, indent=2, ensure_ascii=False))  # ✅ Pretty print JSON
