import re
from transformers import pipeline

# Load AI
ai_worker = pipeline("ner", model="yashpwr/resume-ner-bert-v2", aggregation_strategy="simple")

NAME_BLACKLIST = ["Dxc", "Technology", "Curriculum", "Vitae", "Resume", "Solutions", "Services"]

TECH_SKILLS_DB = [
    "Python", "Java", "C++", "C#", "JavaScript", "React", "Node", "Angular", 
    "SQL", "MongoDB", "AWS", "Docker", "Kubernetes", "Machine Learning", 
    "Data Science", "Blockchain", "Solidity", "HTML", "CSS"
]

EDUCATION_KEYWORDS = {
    "Master's": ["mtech", "m.tech", "ms ", "m.s", "master", "mba", "msc"],
    "Bachelor's": ["btech", "b.tech", "be ", "b.e", "bachelor", "bsc"],
    "PhD": ["phd", "doctorate"]
}

def is_valid_name(name):
    name_lower = name.lower()
    return not any(word.lower() in name_lower for word in NAME_BLACKLIST)

def extract_all(cleaned_text, raw_text=None, candidate_id=None):
    input_text = raw_text if raw_text else cleaned_text
    
    # 1. Name
    name = "Unknown"
    results = ai_worker(input_text[:500])
    for res in results:
        if res['entity_group'] == 'NAME':
            temp_name = res['word'].title()
            if is_valid_name(temp_name) and len(temp_name) > 3:
                name = temp_name
                break
    
    if name == "Unknown" and candidate_id is not None:
        lines = [l.strip() for l in raw_text.split('\n') if len(l.strip()) > 2]
        name = lines[0].title() if lines else f"Candidate_{candidate_id + 101}"

    # 2. Skills
    ai_skills = {res['word'].title() for res in results if res['entity_group'] == 'SKILL'}
    found_tech = [s for s in TECH_SKILLS_DB if re.search(rf'\b{s}\b', cleaned_text, re.IGNORECASE)]
    final_skills = list(ai_skills.union(set(found_tech)))

    # 3. Education
    edu = "Not Specified"
    for level, keys in EDUCATION_KEYWORDS.items():
        if any(k in cleaned_text.lower() for k in keys):
            edu = level
            break

    # 4. Experience (Enhanced Regex)
    exp_match = re.search(r'(\d+)\s*(?:\+|-|to)?\s*(?:\d+)?\s*years?', cleaned_text, re.IGNORECASE)
    experience = f"{exp_match.group(1)} yrs" if exp_match else "Fresher"

    return {"name": name, "education": edu, "experience": experience, "skills": final_skills}
