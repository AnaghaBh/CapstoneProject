import json
from utils.llm_client import call_llm

def load_templates():
    """Load Schema framework templates."""
    with open('data/prompts/schema_templates.json', 'r') as f:
        return json.load(f)

def analyse_claim(claim):
    """Analyze claim using general Schema Theory."""
    templates = load_templates()
    
    # Define schema categories and keywords
    schema_keywords = {
        "health_safety": ["health", "safe", "cure", "virus", "medicine", "treatment"],
        "family_protection": ["family", "children", "protect", "love", "care", "kids"],
        "science_trust": ["study", "research", "scientists", "experts", "evidence"],
        "fairness": ["fair", "equal", "justice", "right", "wrong", "deserve"],
        "environmental_responsibility": ["environment", "climate", "green", "natural", "earth"],
        "government_accountability": ["government", "officials", "policy", "authority"],
        "community_benefit": ["community", "society", "everyone", "public", "together"]
    }
    
    # Detect schema category
    schema_category = "general"
    for category, keywords in schema_keywords.items():
        if any(keyword in claim.lower() for keyword in keywords):
            schema_category = category
            break
    
    # Assess congruence (manipulative vs genuine)
    manipulative_cues = ["shocking", "secret", "hidden", "they don't want you to know"]
    congruent_flag = 0 if any(cue in claim.lower() for cue in manipulative_cues) else 1
    
    # Get LLM analysis
    prompt = templates["analyse_template"].format(claim=claim)
    analysis = call_llm(templates["system"], prompt)
    
    return {
        "schema_category": schema_category,
        "schema_congruent_flag": congruent_flag,
        "schema_cue_explanation": analysis
    }

def simulate_misinformation(params):
    """Generate misinformation using schema manipulation."""
    templates = load_templates()
    schema_category = params.get('schema_category', 'health_safety')
    
    prompt = templates["misinfo_template"].format(schema_category=schema_category)
    misinfo_text = call_llm(templates["system"], prompt)
    
    # Analyze generated misinformation
    metadata = analyse_claim(misinfo_text)
    metadata['target_schema'] = schema_category
    
    return misinfo_text, metadata

def generate_correction(claim, metadata, tone="neutral", cohort="general"):
    """Generate schema-consistent correction."""
    templates = load_templates()
    
    schema_category = metadata.get('schema_category', 'general')
    prompt = templates["correction_template"].format(claim=claim, schema_category=schema_category)
    
    correction_text = call_llm(templates["system"], prompt)
    
    # Analyze correction
    correction_metadata = analyse_claim(correction_text)
    correction_metadata['correction_tone'] = tone
    correction_metadata['target_cohort'] = cohort
    
    return correction_text, correction_metadata