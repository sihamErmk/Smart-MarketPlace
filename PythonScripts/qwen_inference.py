import json
import sys
import re
from openai import OpenAI

def detect_language(text):
    """
    Detect language from text using character analysis
    """
    # Check for common characters in different languages
    arabic_chars = "أبتثجحخدذرزسشصضطظعغفقكلمنهويءة"
    french_chars = "éèêëàâäôöùûüÿçœæ"
    spanish_chars = "áéíóúüñ¿¡"
    
    # Count characters from each language
    arabic_count = sum(1 for char in text if char in arabic_chars)
    french_count = sum(1 for char in text if char in french_chars)
    spanish_count = sum(1 for char in text if char in spanish_chars)
    
    # Determine language based on character count
    if arabic_count > 0:
        return "arabic"
    elif french_count > 0:
        return "french"
    elif spanish_count > 0:
        return "spanish"
    else:
        return "english"  # Default to English

def generate_mission(prompt, language="auto"):
    """
    Generate a job mission using OpenRouter API with Qwen2.5
    """
    try:
        # Auto-detect language if set to auto
        if language == "auto":
            detected_lang = detect_language(prompt)
        else:
            detected_lang = language
            
        # Initialize OpenAI client with OpenRouter base URL and API key
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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",
        )
        
        # Create system prompt based on detected language
        if detected_lang == "french":
            system_prompt = """Tu es un assistant spécialisé dans la création de fiches missions freelance.
À partir d'une brève description, tu dois générer une fiche mission complète.
IMPORTANT: Toute la sortie doit être en français, y compris tous les titres, champs et valeurs.
Réponds UNIQUEMENT au format JSON suivant (sans commentaires) :

{
  "title": "Titre concis et accrocheur de la mission",
  "description": "Description détaillée incluant contexte et objectifs",
  "country": "Nom du pays en français",
  "city": "Nom de la ville en français",
  "workMode": "Un parmi: REMOTE, ONSITE, HYBRID",
  "duration": "Durée (nombre)",
  "durationType": "Unité de durée (MOIS, ANNEE)",
  "startImmediately": true/false,
  "startDate": "Date de début en format yyyy-MM-dd (si startImmediately = false)",
  "experienceYear": "Un parmi: 0-3, 3-7, 7-12, 12+",
  "contractType": "Un parmi: FORFAIT, REGIE",
  "estimatedDailyRate": "Taux journalier moyen en euros (nombre)",
  "domain": "Domaine d'activité principal",
  "position": "Intitulé du poste/fonction",
  "requiredExpertises": ["expertise1", "expertise2", ...],
  "uiLabels": {
    "description": "Description",
    "expertise": "Expertises Requises",
    "details": "Détails de la Mission",
    "position": "Poste",
    "location": "Lieu",
    "workMode": "Mode de Travail",
    "duration": "Durée",
    "experience": "Expérience",
    "contractType": "Type de Contrat",
    "dailyRate": "Taux Journalier",
    "domain": "Domaine"
  }
}"""
        elif detected_lang == "arabic":
            system_prompt = """أنت مساعد متخصص في إنشاء مهام العمل الحر.
من وصف موجز، يجب عليك إنشاء مهمة عمل كاملة.
مهم: يجب أن تكون جميع المخرجات باللغة العربية، بما في ذلك جميع العناوين والحقول والقيم.
الرد فقط بتنسيق JSON التالي (بدون تعليقات):

{
  "title": "عنوان موجز وجذاب للمهمة",
  "description": "وصف مفصل يتضمن السياق والأهداف",
  "country": "اسم البلد بالعربية",
  "city": "اسم المدينة بالعربية",
  "workMode": "واحد من: عن بعد، في الموقع، هجين",
  "duration": "المدة (رقم)",
  "durationType": "وحدة المدة (شهر، سنة)",
  "startImmediately": true/false,
  "startDate": "تاريخ البدء بتنسيق yyyy-MM-dd (إذا كان startImmediately = false)",
  "experienceYear": "واحد من: 0-3، 3-7، 7-12، +12",
  "contractType": "واحد من: ثابت، بالساعة",
  "estimatedDailyRate": "متوسط المعدل اليومي باليورو (رقم)",
  "domain": "مجال النشاط الرئيسي",
  "position": "المسمى الوظيفي",
  "requiredExpertises": ["خبرة1", "خبرة2", ...],
  "uiLabels": {
    "description": "الوصف",
    "expertise": "الخبرات المطلوبة",
    "details": "تفاصيل المهمة",
    "position": "المنصب",
    "location": "الموقع",
    "workMode": "نمط العمل",
    "duration": "المدة",
    "experience": "الخبرة",
    "contractType": "نوع العقد",
    "dailyRate": "المعدل اليومي",
    "domain": "المجال"
  }
}"""
        elif detected_lang == "spanish":
            system_prompt = """Eres un asistente especializado en la creación de misiones freelance.
A partir de una breve descripción, debes generar una misión completa.
IMPORTANTE: Toda la salida debe estar en español, incluyendo todos los títulos, campos y valores.
Responde ÚNICAMENTE en el siguiente formato JSON (sin comentarios):

{
  "title": "Título conciso y atractivo de la misión",
  "description": "Descripción detallada incluyendo contexto y objetivos",
  "country": "Nombre del país en español",
  "city": "Nombre de la ciudad en español",
  "workMode": "Uno entre: REMOTO, PRESENCIAL, HÍBRIDO",
  "duration": "Duración (número)",
  "durationType": "Unidad de duración (MES, AÑO)",
  "startImmediately": true/false,
  "startDate": "Fecha de inicio en formato yyyy-MM-dd (si startImmediately = false)",
  "experienceYear": "Uno entre: 0-3, 3-7, 7-12, 12+",
  "contractType": "Uno entre: PRECIO FIJO, TIEMPO Y MATERIALES",
  "estimatedDailyRate": "Tarifa diaria media en euros (número)",
  "domain": "Dominio de actividad principal",
  "position": "Título del puesto/función",
  "requiredExpertises": ["experiencia1", "experiencia2", ...],
  "uiLabels": {
    "description": "Descripción",
    "expertise": "Experiencia Requerida",
    "details": "Detalles de la Misión",
    "position": "Posición",
    "location": "Ubicación",
    "workMode": "Modo de Trabajo",
    "duration": "Duración",
    "experience": "Experiencia",
    "contractType": "Tipo de Contrato",
    "dailyRate": "Tarifa Diaria",
    "domain": "Dominio"
  }
}"""
        else:
            system_prompt = """You are an assistant specialized in creating freelance job missions.
From a brief description, you must generate a complete job mission.
IMPORTANT: All output must be in English, including all titles, fields, and values.
Respond ONLY in the following JSON format (without comments):

{
  "title": "Concise and catchy mission title",
  "description": "Detailed description including context and objectives",
  "country": "Country name in English",
  "city": "City name in English",
  "workMode": "One of: REMOTE, ONSITE, HYBRID",
  "duration": "Duration (number)",
  "durationType": "Duration unit (MONTH, YEAR)",
  "startImmediately": true/false,
  "startDate": "Start date in yyyy-MM-dd format (if startImmediately = false)",
  "experienceYear": "One of: 0-3, 3-7, 7-12, 12+",
  "contractType": "One of: FIXED_PRICE, TIME_AND_MATERIALS",
  "estimatedDailyRate": "Average daily rate in euros (number)",
  "domain": "Main activity domain",
  "position": "Job title/function",
  "requiredExpertises": ["expertise1", "expertise2", ...],
  "uiLabels": {
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
        Make sure ALL fields in the response are in the SAME LANGUAGE as the system prompt.
        Include a "uiLabels" object with all UI labels translated to the appropriate language.
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
                # Add detected language to the response
                mission_data["detectedLanguage"] = detected_lang
                return json.dumps(mission_data, indent=2)
            else:
                # Try to parse the entire response as JSON
                mission_data = json.loads(response)
                # Add detected language to the response
                mission_data["detectedLanguage"] = detected_lang
                return json.dumps(mission_data, indent=2)
        except Exception as e:
            return json.dumps({
                "error": f"Error parsing JSON: {str(e)}",
                "raw_response": response,
                "detectedLanguage": detected_lang
            })
            
    except Exception as e:
        return json.dumps({
            "error": f"API Error: {str(e)}",
            "detectedLanguage": language if language != "auto" else "english"
        })

# Fallback to a mock implementation if the API fails
def generate_mock_mission(prompt, language="auto"):
    """
    Generate a mock mission for testing without requiring the API
    """
    # Auto-detect language if set to auto
    if language == "auto":
        detected_lang = detect_language(prompt)
    else:
        detected_lang = language
    
    # Extract technology/skill from prompt
    tech = prompt.split()[0] if prompt else "general"
    
    # Create mock mission based on detected language
    if detected_lang == "french":
        mock_mission = {
            "title": f"Expert en {tech.title()} Recherché",
            "description": f"## Contexte\nNotre client recherche un expert en {tech} pour un projet de développement.\n\n## Responsabilités\n- Développer des solutions {tech}\n- Collaborer avec les membres de l'équipe\n- Livrer un travail de haute qualité\n\n## Exigences\n- Expérience avec {tech}\n- Bonnes compétences en communication\n- Souci du détail",
            "country": "France",
            "city": "Paris",
            "workMode": "REMOTE",
            "duration": 3,
            "durationType": "MOIS",
            "startImmediately": True,
            "startDate": "",
            "experienceYear": "3-7",
            "contractType": "FORFAIT",
            "estimatedDailyRate": 400,
            "domain": "Technologie",
            "position": f"Spécialiste {tech.title()}",
            "requiredExpertises": [tech.title(), "Communication", "Gestion de Projet"],
            "uiLabels": {
                "description": "Description",
                "expertise": "Expertises Requises",
                "details": "Détails de la Mission",
                "position": "Poste",
                "location": "Lieu",
                "workMode": "Mode de Travail",
                "duration": "Durée",
                "experience": "Expérience",
                "contractType": "Type de Contrat",
                "dailyRate": "Taux Journalier",
                "domain": "Domaine"
            },
            "detectedLanguage": detected_lang
        }
    elif detected_lang == "arabic":
        mock_mission = {
            "title": f"مطلوب خبير في {tech.title()}",
            "description": f"## السياق\nيبحث عميلنا عن خبير في {tech} لمشروع تطوير.\n\n## المسؤوليات\n- تطوير حلول {tech}\n- التعاون مع أعضاء الفريق\n- تقديم عمل عالي الجودة\n\n## المتطلبات\n- خبرة في {tech}\n- مهارات تواصل جيدة\n- الاهتمام بالتفاصيل",
            "country": "المغرب",
            "city": "الدار البيضاء",
            "workMode": "عن بعد",
            "duration": 3,
            "durationType": "شهر",
            "startImmediately": True,
            "startDate": "",
            "experienceYear": "3-7",
            "contractType": "ثابت",
            "estimatedDailyRate": 400,
            "domain": "تكنولوجيا",
            "position": f"متخصص {tech.title()}",
            "requiredExpertises": [tech.title(), "مهارات التواصل", "إدارة المشاريع"],
            "uiLabels": {
                "description": "الوصف",
                "expertise": "الخبرات المطلوبة",
                "details": "تفاصيل المهمة",
                "position": "المنصب",
                "location": "الموقع",
                "workMode": "نمط العمل",
                "duration": "المدة",
                "experience": "الخبرة",
                "contractType": "نوع العقد",
                "dailyRate": "المعدل اليومي",
                "domain": "المجال"
            },
            "detectedLanguage": detected_lang
        }
    elif detected_lang == "spanish":
        mock_mission = {
            "title": f"Se Busca Experto en {tech.title()}",
            "description": f"## Contexto\nNuestro cliente busca un experto en {tech} para un proyecto de desarrollo.\n\n## Responsabilidades\n- Desarrollar soluciones de {tech}\n- Colaborar con los miembros del equipo\n- Entregar trabajo de alta calidad\n\n## Requisitos\n- Experiencia con {tech}\n- Buenas habilidades de comunicación\n- Atención al detalle",
            "country": "España",
            "city": "Madrid",
            "workMode": "REMOTO",
            "duration": 3,
            "durationType": "MES",
            "startImmediately": True,
            "startDate": "",
            "experienceYear": "3-7",
            "contractType": "PRECIO FIJO",
            "estimatedDailyRate": 400,
            "domain": "Tecnología",
            "position": f"Especialista en {tech.title()}",
            "requiredExpertises": [tech.title(), "Comunicación", "Gestión de Proyectos"],
            "uiLabels": {
                "description": "Descripción",
                "expertise": "Experiencia Requerida",
                "details": "Detalles de la Misión",
                "position": "Posición",
                "location": "Ubicación",
                "workMode": "Modo de Trabajo",
                "duration": "Duración",
                "experience": "Experiencia",
                "contractType": "Tipo de Contrato",
                "dailyRate": "Tarifa Diaria",
                "domain": "Dominio"
            },
            "detectedLanguage": detected_lang
        }
    else:
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
            "uiLabels": {
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
            },
            "detectedLanguage": detected_lang
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