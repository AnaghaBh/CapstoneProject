import re
import json
import os
from utils.llm_client import call_llm

def load_templates():
    """Load ELM framework templates."""
    with open('data/prompts/elm_templates.json', 'r') as f:
        return json.load(f)

def analyse_claim(claim):
    """Analyze claim using Elaboration Likelihood Model."""
    templates = load_templates()
    
    # Detect central cues
    central_patterns = r'\b(study|research|data|statistics|according to|shows that|evidence|peer-reviewed)\b'
    central_cues = len(re.findall(central_patterns, claim.lower()))
    
    # Detect peripheral cues  
    peripheral_patterns = r'\b(shocking|everyone|amazing|incredible|must|urgent|believe|trust me)\b'
    peripheral_cues = len(re.findall(peripheral_patterns, claim.lower()))
    
    # Calculate scores
    central_score = min(central_cues / 3.0, 1.0)
    peripheral_score = min(peripheral_cues / 3.0, 1.0)
    
    # Classify route
    if central_score > peripheral_score:
        elm_label = "central"
    elif peripheral_score > central_score:
        elm_label = "peripheral"
    else:
        elm_label = "mixed"
    
    # Get LLM analysis
    prompt = templates["analyse_template"].format(claim=claim)
    analysis = call_llm(templates["system"], prompt)
    
    return {
        "central_cue_score": central_score,
        "peripheral_cue_score": peripheral_score,
        "elm_label": elm_label,
        "elm_rationale": analysis
    }

def simulate_misinformation(params):
    """Generate misinformation using ELM principles."""
    templates = load_templates()
    route = params.get('route', 'peripheral')
    
    prompt = templates["misinfo_template"].format(route=route)
    misinfo_text = call_llm(templates["system"], prompt)
    
    # Analyze generated misinformation
    metadata = analyse_claim(misinfo_text)
    metadata['generation_route'] = route
    
    return misinfo_text, metadata

def generate_correction(claim, metadata, tone="neutral", cohort="general"):
    """Generate correction using central route approach."""
    templates = load_templates()
    
    route = metadata.get('elm_label', 'peripheral')
    prompt = templates["correction_template"].format(claim=claim, route=route)
    
    correction_text = call_llm(templates["system"], prompt)
    
    # Analyze correction
    correction_metadata = analyse_claim(correction_text)
    correction_metadata['correction_tone'] = tone
    correction_metadata['target_cohort'] = cohort
    
    return correction_text, correction_metadata