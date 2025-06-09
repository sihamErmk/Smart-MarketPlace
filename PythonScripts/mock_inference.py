import json
import sys

def generate_mock_mission(prompt, language="english"):
    """
    Generate a mock mission for testing without requiring the Hugging Face model
    """
    # Create a mock response based on the prompt
    keywords = prompt.split(',')
    main_keyword = keywords[0].strip() if keywords else "general"
    
    mock_mission = {
        "title": f"{main_keyword.capitalize()} Expert Needed for Exciting Project",
        "description": f"## Responsibilities\n- Work on {main_keyword} related tasks\n- Collaborate with team members\n- Deliver high-quality work\n\n## Requirements\n- Experience with {main_keyword}\n- Good communication skills\n- Attention to detail",
        "country": "Morocco",
        "city": "Casablanca",
        "workMode": "REMOTE",
        "duration": 3,
        "durationType": "MONTH",
        "startImmediately": True,
        "startDate": "",
        "experienceYear": "3-7",
        "contractType": "FORFAIT",
        "estimatedDailyRate": 200,
        "domain": "Technology",
        "position": f"{main_keyword.capitalize()} Specialist",
        "requiredExpertises": [main_keyword.capitalize(), "Communication", "Project Management"]
    }
    
    return json.dumps(mock_mission, indent=2)

if __name__ == "__main__":
    # Get input from command line arguments
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No prompt provided"}))
        sys.exit(1)
    
    prompt = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "english"
    
    # Generate and print the mock mission
    result = generate_mock_mission(prompt, language)
    print(result)