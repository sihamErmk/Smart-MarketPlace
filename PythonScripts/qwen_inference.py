import json
import sys
import re
from openai import OpenAI

def generate_mission(prompt, language="auto"):
    """
    Generate a job mission using OpenRouter API with Qwen2.5
    """
    try:
        # Initialize OpenAI client with OpenRouter base URL and API key
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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",
        )
        
        # Create system prompt that works for any language
        system_prompt = """You are an assistant specialized in creating freelance job missions.
From the user's input, generate a complete job mission in the SAME LANGUAGE as the input.
ALL output fields, labels, and values must be in the SAME LANGUAGE as the input.

Respond ONLY in the following JSON format (without comments):

{
  "title": "Mission title in the input language",
  "description": "Detailed description in the input language",
  "country": "Country name in the input language",
  "city": "City name in the input language",
  "workMode": "Work mode in the input language",
  "duration": Number,
  "durationType": "Duration type in the input language",
  "startImmediately": true/false,
  "startDate": "Date in yyyy-MM-dd format if not starting immediately",
  "experienceYear": "Experience range in the input language",
  "contractType": "Contract type in the input language",
  "estimatedDailyRate": Number,
  "domain": "Domain/industry in the input language",
  "position": "Position title in the input language",
  "requiredExpertises": ["Expertise 1 in input language", "Expertise 2 in input language", ...],
  "uiLabels": {
    "description": "Description label in input language",
    "expertise": "Required expertise label in input language",
    "details": "Mission details label in input language",
    "position": "Position label in input language",
    "location": "Location label in input language",
    "workMode": "Work mode label in input language",
    "duration": "Duration label in input language",
    "experience": "Experience label in input language",
    "contractType": "Contract type label in input language",
    "dailyRate": "Daily rate label in input language",
    "domain": "Domain label in input language"
  }
}"""
        
        # Create user prompt with detailed instructions
        user_prompt = f"""
        Analyze this job mission request and generate a complete job mission: {prompt}
        
        Extract all relevant information from the request, including:
        - Skills and technologies
        - Budget or rate
        - Location (city, country)
        - Work mode
        - Duration
        - Experience level
        - Contract type
        - Domain/industry
        
        If any information is missing, use reasonable defaults based on the context.
        Make sure ALL fields in the response are in the SAME LANGUAGE as the input.
        Include a "uiLabels" object with all UI labels translated to the input language.
        """
        
        # Call the API
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://smartmarketplace.local",
                "X-Title": "Smart MarketPlace",
            },
            extra_body={
                "allow_training": True
            },
            model="qwen/qwen2.5-vl-3b-instruct:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        # Extract the response
        response = completion.choices[0].message.content
        
        # Try to extract JSON from the response
        try:
            # Find JSON content between curly braces if needed
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                # Parse and format JSON
                mission_data = json.loads(json_str)
                return json.dumps(mission_data, indent=2)
            else:
                # Try to parse the entire response as JSON
                mission_data = json.loads(response)
                return json.dumps(mission_data, indent=2)
        except Exception as e:
            return json.dumps({
                "error": f"Error parsing JSON: {str(e)}",
                "raw_response": response
            })
            
    except Exception as e:
        return json.dumps({
            "error": f"API Error: {str(e)}"
        })

# Fallback to a mock implementation if the API fails
def generate_mock_mission(prompt, language="auto"):
    """
    Generate a mock mission for testing without requiring the API
    """
    # Extract technology/skill from prompt
    tech = prompt.split()[0] if prompt else "general"
    
    # Default UI labels in English
    ui_labels = {
        "description": "Description",
        "expertise": "Required Expertise",
        "details": "Mission Details",
        "position": "Position",
        "location": "Location",
        "workMode": "Work Mode",
        "duration": "Duration",
        "experience": "Experience",
        "contractType": "Contract Type",
        "dailyRate": "Daily Rate",
        "domain": "Domain"
    }
    
    # Create mock mission with default values
    mock_mission = {
        "title": f"{tech.title()} Expert Needed",
        "description": f"## Context\nOur client is looking for a {tech} expert for a development project.\n\n## Responsibilities\n- Develop {tech} solutions\n- Collaborate with team members\n- Deliver high-quality work\n\n## Requirements\n- Experience with {tech}\n- Good communication skills\n- Attention to detail",
        "country": "United States",
        "city": "New York",
        "workMode": "REMOTE",
        "duration": 3,
        "durationType": "MONTH",
        "startImmediately": True,
        "startDate": "",
        "experienceYear": "3-7",
        "contractType": "FIXED_PRICE",
        "estimatedDailyRate": 400,
        "domain": "Technology",
        "position": f"{tech.title()} Specialist",
        "requiredExpertises": [tech.title(), "Communication", "Project Management"],
        "uiLabels": ui_labels
    }
    
    return json.dumps(mock_mission, indent=2)

if __name__ == "__main__":
    # Get input from command line arguments
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No prompt provided"}))
        sys.exit(1)
    
    prompt = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "auto"
    
    # Try to use the API first, fall back to mock if it fails
    try:
        result = generate_mission(prompt, language)
        # Check if there was an API error
        if '"error":' in result:
            print(generate_mock_mission(prompt, language))
        else:
            print(result)
    except Exception:
        # Fall back to mock implementation
        print(generate_mock_mission(prompt, language))