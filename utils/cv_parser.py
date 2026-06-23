import re
from collections import Counter

# ============ 1. COMPÉTENCES PRÉDÉFINIES PAR DOMAINE ============

SKILLS_BY_DOMAIN = {
    "data_science": [
        "Python", "SQL", "Pandas", "NumPy", "Scikit-learn", "TensorFlow",
        "PyTorch", "Keras", "Machine Learning", "Deep Learning", "NLP",
        "Computer Vision", "Data Visualization", "Tableau", "Power BI",
        "Spark", "Hadoop", "Big Data", "Statistics", "Probability",
        "A/B Testing", "Feature Engineering", "Model Deployment"
    ],
    "software_engineering": [
        "Python", "Java", "C++", "JavaScript", "TypeScript", "React",
        "Angular", "Vue.js", "Node.js", "Django", "Flask", "FastAPI",
        "Spring Boot", "Docker", "Kubernetes", "AWS", "Azure", "GCP",
        "Git", "CI/CD", "Agile", "Scrum", "Microservices", "REST API",
        "GraphQL", "MongoDB", "PostgreSQL", "MySQL", "Redis"
    ],
    "finance": [
        "Financial Analysis", "Risk Management", "Portfolio Management",
        "Bloomberg", "Excel", "VBA", "SAP", "QuickBooks", "Financial Modeling",
        "M&A", "Derivatives", "Asset Management", "Compliance", "Audit",
        "Cash Flow Analysis", "Budgeting", "Forecasting", "CPA", "CFA"
    ],
    "marketing": [
        "Digital Marketing", "SEO", "SEM", "Google Analytics", "Social Media",
        "Content Marketing", "Email Marketing", "Marketing Automation",
        "HubSpot", "Salesforce", "CRM", "Brand Strategy", "Market Research",
        "PPC", "Copywriting", "Storytelling", "A/B Testing", "Conversion Rate",
        "Customer Journey", "Marketing Analytics"
    ],
    "hr": [
        "Talent Acquisition", "Recruitment", "Onboarding", "HRIS", "SAP SuccessFactors",
        "Employee Relations", "Performance Management", "Training & Development",
        "Compensation & Benefits", "Workforce Planning", "Labor Law",
        "Organizational Development", "Diversity & Inclusion", "ATS"
    ],
    "design": [
        "UX Design", "UI Design", "Figma", "Sketch", "Adobe XD", "Photoshop",
        "Illustrator", "InDesign", "Prototyping", "Wireframing", "User Research",
        "Design Systems", "Visual Design", "Product Design", "Typography",
        "Brand Identity", "Motion Design", "After Effects"
    ],
    "general": [
        "Leadership", "Project Management", "Agile", "Scrum", "Communication",
        "Team Management", "Problem Solving", "Critical Thinking", "Time Management",
        "Adaptability", "Collaboration", "Public Speaking", "Writing",
        "Data Analysis", "Decision Making", "Strategic Planning"
    ]
}

# ============ 2. LISTE DE TOUTES LES COMPÉTENCES ============

ALL_SKILLS = []
for skills in SKILLS_BY_DOMAIN.values():
    ALL_SKILLS.extend(skills)
ALL_SKILLS = list(set(ALL_SKILLS))

# ============ 3. MOTS-CLÉS POUR DÉTECTION AUTOMATIQUE DU DOMAINE ============

DOMAIN_KEYWORDS = {
    "data_science": ["machine learning", "deep learning", "data science", "neural network", "nlp", "tensorflow", "pytorch", "scikit-learn", "data mining", "big data", "spark", "hadoop", "statistics", "probability", "data visualization", "a/b testing", "feature engineering"],
    "software_engineering": ["software engineer", "full stack", "react", "angular", "vue", "node.js", "django", "flask", "spring", "kubernetes", "docker", "microservices", "rest api", "graphql", "cloud", "aws", "azure", "gcp"],
    "finance": ["financial", "risk", "portfolio", "invest", "merger", "acquisition", "budget", "forecasting", "compliance", "audit", "cpa", "cfa", "capital", "asset", "derivative"],
    "marketing": ["marketing", "seo", "sem", "social media", "content", "brand", "customer", "campaign", "analytics", "crm", "automation"],
    "hr": ["recruitment", "talent", "onboarding", "employee", "hr", "human resources", "compensation", "benefits", "training", "workforce"],
    "design": ["ux", "ui", "figma", "sketch", "adobe", "prototype", "wireframe", "design system", "typography"]
}

# ============ 4. FONCTION DE DÉTECTION DU DOMAINE ============

def detect_domain(text, custom_domain=None):
    """
    Détecte automatiquement le domaine du CV
    Si custom_domain est fourni, l'utilise directement
    """
    # Si un domaine personnalisé est fourni, l'utiliser
    if custom_domain:
        return custom_domain
    
    text_lower = text.lower()
    domain_scores = {}
    
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text_lower:
                score += 1
        domain_scores[domain] = score
    
    if domain_scores:
        best_domain = max(domain_scores, key=domain_scores.get)
        if domain_scores[best_domain] > 0:
            return best_domain
    
    return "general"

# ============ 5. FONCTION PRINCIPALE : DÉTECTION DES COMPÉTENCES ============

def detect_skills(text, custom_skills=None, domain=None, user_domain=None):
    """
    Détecte les compétences dans un CV
    
    Args:
        text (str): Texte du CV
        custom_skills (list, optional): Compétences personnalisées par l'utilisateur
        domain (str, optional): Domaine (détection auto si None)
        user_domain (str, optional): Domaine saisi par l'utilisateur (prioritaire)
    
    Returns:
        dict: {
            "found": liste des compétences trouvées,
            "domain": domaine détecté,
            "domain_type": "auto" ou "manual",
            "skills_list": compétences utilisées pour la recherche
        }
    """
    text_lower = text.lower()
    
    # 1. Déterminer le domaine
    domain_type = "auto"
    if user_domain and user_domain.strip():
        # L'utilisateur a saisi un domaine personnalisé
        detected_domain = user_domain.strip().lower().replace(" ", "_")
        domain_type = "manual"
        print(f"📌 Domaine saisi par l'utilisateur: {detected_domain}")
    else:
        # Détection automatique
        detected_domain = detect_domain(text) if domain is None else domain
        print(f"🔍 Domaine détecté automatiquement: {detected_domain}")
    
    # 2. Compétences à chercher
    skills_to_search = []
    
    # 2a. Compétences prédéfinies du domaine (si connu)
    if detected_domain in SKILLS_BY_DOMAIN:
        skills_to_search.extend(SKILLS_BY_DOMAIN[detected_domain])
    
    # 2b. Compétences "general"
    skills_to_search.extend(SKILLS_BY_DOMAIN["general"])
    
    # 2c. NOUVEAU : Compétences personnalisées de l'utilisateur
    if custom_skills and len(custom_skills) > 0:
        # Si l'utilisateur a saisi "une par ligne" ou une liste
        if isinstance(custom_skills, list):
            skills_to_search.extend([s.strip() for s in custom_skills if s.strip()])
        else:
            # Si c'est une chaîne, la découper
            if isinstance(custom_skills, str):
                skills_list = re.split(r'[,;\n]', custom_skills)
                skills_to_search.extend([s.strip() for s in skills_list if s.strip()])
        print(f"📝 Compétences personnalisées ajoutées ({len(skills_to_search)})")
    
    # Supprimer les doublons
    skills_to_search = list(set(skills_to_search))
    
    # 3. Rechercher les compétences dans le texte
    found_skills = []
    found_skills_with_context = []
    
    for skill in skills_to_search:
        if skill.lower() in text_lower:
            found_skills.append(skill)
            
            # Récupérer le contexte
            pattern = r'(.{0,30})' + re.escape(skill) + r'(.{0,30})'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                context = f"...{match.group(1)}{skill}{match.group(2)}..."
                found_skills_with_context.append({
                    "skill": skill,
                    "context": context
                })
    
    return {
        "found": found_skills,
        "domain": detected_domain,
        "domain_type": domain_type,
        "skills_list": skills_to_search,
        "found_with_context": found_skills_with_context,
        "user_provided_skills": custom_skills if custom_skills else []
    }

# ============ 6. FONCTION POUR EXTRAIRE LES COMPÉTENCES AUTO ============

def extract_skills_auto(text, min_mentions=2, additional_keywords=None):
    """
    Extrait automatiquement des compétences du texte (même non listées)
    """
    skill_patterns = [
        r'(?:compétence|skill|connaissance|maîtrise|expertise)(?:s)?\s*:?\s*([^.\n]+)',
        r'(?:langage|technologie|framework|bibliothèque|outil)(?:s)?\s*:?\s*([^.\n]+)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})(?=\s*(?:,|et|\n))'
    ]
    
    found_skills = []
    for pattern in skill_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            skills = re.split(r'[,;\n]', match)
            for skill in skills:
                skill = skill.strip()
                if len(skill) > 2 and len(skill) < 50:
                    found_skills.append(skill)
    
    # Ajouter des mots-clés supplémentaires
    if additional_keywords:
        for keyword in additional_keywords:
            if keyword in text:
                found_skills.append(keyword)
    
    skill_counts = Counter(found_skills)
    return [skill for skill, count in skill_counts.items() 
            if count >= min_mentions and len(skill) > 3]

# ============ 7. FONCTION DE SCORING AVANCÉ ============

def calculate_score(skills_result, required_skills=None, weight_user_skills=0.5):
    """
    Calcule un score avancé avec pondération
    """
    found = skills_result["found"]
    domain = skills_result["domain"]
    user_skills = skills_result.get("user_provided_skills", [])
    
    # Score de base : 5 points par compétence
    base_score = len(found) * 5
    
    # Bonus pour les compétences spécifiques au domaine
    domain_bonus = 0
    if domain in SKILLS_BY_DOMAIN:
        domain_skills = SKILLS_BY_DOMAIN[domain]
        domain_skills_found = [s for s in found if s in domain_skills]
        domain_bonus = len(domain_skills_found) * 3
    
    #  Bonus pour les compétences saisies par l'utilisateur
    user_bonus = 0
    if user_skills:
        user_skills_found = [s for s in found if s in user_skills]
        user_bonus = len(user_skills_found) * int(weight_user_skills * 10)
    
    # Bonus pour les compétences requises
    required_bonus = 0
    if required_skills:
        required_found = [s for s in found if s in required_skills]
        required_bonus = len(required_found) * 5
    
    total = base_score + domain_bonus + user_bonus + required_bonus
    return min(total, 100)

# ============ 8. COMPÉTENCES RECOMMANDÉES POUR UN POSTE ============

def get_skills_for_job(role):
    """
    Retourne des compétences recommandées pour un poste
    """
    job_skills = {
        "data_scientist": ["Python", "SQL", "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "TensorFlow", "Scikit-learn", "Statistics", "Data Visualization", "Big Data", "Spark", "Tableau"],
        "data_analyst": ["SQL", "Excel", "Power BI", "Tableau", "Python", "Data Visualization", "Statistics", "Business Analysis", "R", "Dbt", "Looker"],
        "software_engineer": ["Python", "Java", "C++", "JavaScript", "React", "Node.js", "Django", "Spring Boot", "Docker", "AWS", "Git", "REST API"],
        "devops": ["Docker", "Kubernetes", "AWS", "Azure", "GCP", "Jenkins", "Terraform", "CI/CD", "Linux", "Monitoring", "Python", "Shell"],
        "marketing_manager": ["Digital Marketing", "SEO", "SEM", "Content Marketing", "Social Media", "Analytics", "CRM", "HubSpot", "Salesforce", "Campaign Management"],
        "hr_manager": ["Talent Acquisition", "Employee Relations", "HRIS", "Performance Management", "Training & Development", "Compensation & Benefits", "Labor Law"],
        "ux_designer": ["UX Design", "UI Design", "Figma", "Sketch", "Adobe XD", "User Research", "Prototyping", "Wireframing", "Design Systems"],
        "product_manager": ["Product Strategy", "Roadmapping", "Agile", "Scrum", "Market Research", "User Stories", "Data Analysis", "Project Management"]
    }
    return job_skills.get(role.lower().replace(" ", "_"), [])