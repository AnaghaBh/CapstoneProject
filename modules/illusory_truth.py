import json
from utils.llm_client import call_llm

def load_templates():
    """Load Illusory Truth framework templates."""
    with open('data/prompts/illusory_templates.json', 'r') as f:
        return json.load(f)

def analyse_claim(claim):
    """Analyze claim using Illusory Truth Effect principles."""
    templates = load_templates()
    
    # Detect repetition cues
    repetition_cues = ["everyone knows", "people say", "always", "never", "common knowledge", 
                      "we all know", "it's obvious", "clearly", "obviously"]
    repeat_count = sum(1 for cue in repetition_cues if cue in claim.lower())
    
    # Assess fluency (simple words, familiar concepts)
    words = claim.split()
    simple_words = len([w for w in words if len(w) <= 6])
    fluency_score = min(simple_words / len(words), 1.0) if words else 0
    
    # Determine illusory truth label
    illusory_label = 1 if repeat_count > 0 or fluency_score > 0.7 else 0
    
    # Get LLM analysis
    prompt = templates["analyse_template"].format(claim=claim)
    analysis = call_llm(templates["system"], prompt)
    
    return {
        "repeat_count": repeat_count,
        "fluency_score": fluency_score,
        "illusory_truth_label": illusory_label,
        "repetition_analysis": analysis
    }

def simulate_misinformation(params):
    """Generate misinformation designed for repetition and familiarity."""
    templates = load_templates()
    repetition_level = params.get('repetition_level', 'high')
    
    prompt = templates["misinfo_template"].format(repetition_level=repetition_level)
    misinfo_text = call_llm(templates["system"], prompt)
    
    # Analyze generated misinformation
    metadata = analyse_claim(misinfo_text)
    metadata['target_repetition'] = repetition_level
    
    return misinfo_text, metadata

def generate_correction(claim, metadata, tone="neutral", cohort="general"):
    """Generate correction that disrupts familiarity and repetition."""
    templates = load_templates()
    
    prompt = templates["correction_template"].format(claim=claim)
    correction_text = call_llm(templates["system"], prompt)
    
    # Analyze correction
    correction_metadata = analyse_claim(correction_text)
    correction_metadata['correction_tone'] = tone
    correction_metadata['target_cohort'] = cohort
    
    return correction_text, correction_metadata