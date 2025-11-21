# Misinformation LLM Agent

This project implements a hybrid psychological framework architecture for misinformation research, enabling full X-Y experimental mapping where misinformation can be generated using framework X and corrected using framework Y.

The system provides a comprehensive experimental platform for testing psychological approaches to misinformation correction, with specialized framework modules and a central controller for orchestrating experiments.

## Installation

### 1. Install Ollama
Download and install Ollama from https://ollama.ai/

### 2. Pull the LLaMA model
```bash
ollama pull llama3:8b
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Run the hybrid architecture demo
```bash
python experiments/run_demo.py
```

### Use the central controller
```python
from controller import MisinformationController

controller = MisinformationController()
result = controller.run_experiment(
    claim="Your misinformation claim",
    participant_id="P001",
    cohort="general"
)
```

### Run full framework matrix
```python
# Test all X to Y combinations
results = controller.run_full_matrix(
    claims=["claim1", "claim2"],
    participant_ids=["P001", "P002"]
)
```

## Architecture

### Central Controller
- **`controller.py`** - Orchestrates misinformation to correction experiments
- Supports X to Y framework mapping for comprehensive testing
- Handles participant management and belief assessment
- Logs complete experimental data with metadata

### Specialized Framework Modules
Each module in `modules/` implements:
- `analyse_claim(claim)` - metadata analysis
- `simulate_misinformation(params)` - generate framework-specific misinformation
- `generate_correction(claim, metadata, tone, cohort)` - targeted corrections

## Psychological Frameworks

1. **ELM (Elaboration Likelihood Model)** - Central vs peripheral route processing
2. **FTT (Fuzzy Trace Theory)** - Gist vs verbatim information encoding
3. **Schema Theory** - General cultural schema activation (health, family, science, etc.)
4. **Illusory Truth Effect** - Repetition and familiarity-based belief formation

## Experimental Pipeline
1. **Input**: Original claim + participant ID + cohort
2. **Framework Selection**: Choose misinformation framework X and correction framework Y
3. **Analysis**: Analyze claim using framework X methodology
4. **Simulation**: Generate misinformation using framework X principles
5. **Belief Assessment**: Measure initial belief in misinformation (placeholder)
6. **Correction**: Generate correction using framework Y approach
7. **Evaluation**: Measure post-correction belief (placeholder)
8. **Logging**: Record complete experimental data with metadata

## File Structure
```
controller.py              # Central experiment orchestrator
modules/
  ├── elm_general.py       # Elaboration Likelihood Model
  ├── ftt.py              # Fuzzy Trace Theory
  ├── schema_general.py    # Schema Theory (general)
  └── illusory_truth.py    # Illusory Truth Effect
utils/
  ├── llm_client.py       # Ollama LLM interface
  ├── logging_utils.py    # Experiment logging
  └── safety.py           # Content safety checks
data/
  ├── prompts/
  │   ├── elm_templates.json      # ELM-specific prompts
  │   ├── ftt_templates.json      # FTT-specific prompts
  │   ├── schema_templates.json   # Schema-specific prompts
  │   └── illusory_templates.json # Illusory Truth prompts
  ├── outputs/
  │   └── corrections_log.csv     # Experiment results
  └── sample_claims.csv           # Sample misinformation claims
experiments/
  └── run_demo.py         # Demo script
config/
  └── settings.yaml       # Configuration settings
requirements.txt         # Python dependencies
```