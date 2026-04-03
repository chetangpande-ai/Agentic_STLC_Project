import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.requirement_analyzer import analyze_requirement

# Example test input
def main():
    requirement_raw = "The system shall allow users to reset their password via email verification."
    application_context = {
        "platform": "Web",
        "user_roles": ["admin", "user"],
        "security": "OAuth2, HTTPS"
    }
    reviewer_feedback = "Consider edge cases for invalid email and rate limiting."

    result = analyze_requirement(requirement_raw, application_context, reviewer_feedback)
    print("\n--- Requirement Analysis Result ---\n")
    print(result)

if __name__ == "__main__":
    main()
