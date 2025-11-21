import json
from utils.llm_client import call_llm

def load_templates():
    """Load FTT framework templates."""
    with open('data/prompts/ftt_templates.json', 'r') as f:
        return json.load(f)

def analyse_claim(claim):
    """Analyze claim using Fuzzy Trace Theory."""
    templates = load_templates()
    
    # Extract gist (simplified version)
    words = claim.split()
    gist_text = " ".join(words[:10]) if len(words) > 10 else claim
    verbatim_text = claim
    
    # Calculate similarity
    similarity = min(len(gist_text) / len(verbatim_text), 1.0)
    
    # Detect distortion markers
    distortion_markers = ["all", "never", "always", "instantly", "completely", "totally"]
    distortion_flag = 1 if any(marker in claim.lower() for marker in distortion_markers) else 0
    
    # Get LLM analysis
    prompt = templates["analyse_template"].format(claim=claim)
    analysis = call_llm(templates["system"], prompt)
    
    return {
        "gist_text": gist_text,
        "verbatim_text": verbatim_text,
        "gist_detail_similarity": similarity,
        "ftt_distortion_flag": distortion_flag,
        "discrepancy_explanation": analysis
    }

def simulate_misinformation(params):
    """Generate misinformation using FTT distortion principles."""
    templates = load_templates()
    topic = params.get('topic', 'health')
    
    prompt = templates["misinfo_template"].format(topic=topic)
    misinfo_text = call_llm(templates["system"], prompt)
    
    # Analyze generated misinformation
    metadata = analyse_claim(misinfo_text)
    metadata['generation_topic'] = topic
    
    return misinfo_text, metadata

def generate_correction(claim, metadata, tone="neutral", cohort="general"):
    """Generate correction highlighting gist-verbatim discrepancy."""
    templates = load_templates()
    
    gist = metadata.get('gist_text', claim)
    prompt = templates["correction_template"].format(claim=claim, gist=gist)
    
    correction_text = call_llm(templates["system"], prompt)
    
    # Analyze correction
    correction_metadata = analyse_claim(correction_text)
    correction_metadata['correction_tone'] = tone
    correction_metadata['target_cohort'] = cohort
    
    return correction_text, correction_metadata