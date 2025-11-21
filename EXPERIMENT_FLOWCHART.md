# Misinformation Experiment Flowchart

## Complete Experimental Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             EXPERIMENT SETUP                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. INITIALIZE CONTROLLER                                                   │
│     from controller import MisinformationController                         │
│     controller = MisinformationController()                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  2. CHOOSE EXPERIMENT TYPE                                                  │
│     ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐       │
│     │ Single          │    │ Batch           │    │ Full Matrix     │       │
│     │ Experiment      │    │ Experiments     │    │ (All X→Y)       │       │
│     └─────────────────┘    └─────────────────┘    └─────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
                │                        │                        │
                ▼                        ▼                        ▼
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   SINGLE EXPERIMENT │    │   BATCH EXPERIMENTS │    │   FULL MATRIX       │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
                │                        │                        │
                ▼                        ▼                        ▼

═══════════════════════════════════════════════════════════════════════════════
                            SINGLE EXPERIMENT FLOW
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│  INPUT PARAMETERS                                                           │
│  • claim = "Original misinformation claim"                                  │
│  • participant_id = "P001"                                                  │
│  • cohort = "student"                                                       │
│  • misinfo_framework = "elm_general" (optional)                             │
│  • correction_framework = "ftt" (optional)                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  FRAMEWORK SELECTION                                                        │
│  If not specified:                                                          │
│  • Randomly select misinformation framework X                               │
│  • Randomly select correction framework Y                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1: ANALYZE ORIGINAL CLAIM                                             │
│  Framework X.analyse_claim(claim)                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ ELM: Central/peripheral cues → scores, labels                       │    │
│  │ FTT: Gist/verbatim extraction → similarity, distortion              │    │
│  │ Schema: Cultural schema detection → category, congruence            │    │
│  │ Illusory: Repetition cues → fluency, familiarity                    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 2: SIMULATE MISINFORMATION                                            │
│  Framework X.simulate_misinformation(params)                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ ELM: Generate peripheral (emotional) or central (fake stats)        │    │
│  │ FTT: Create distorted gist with exaggerated claims                  │    │
│  │ Schema: Exploit cultural values (family, health, safety)            │    │
│  │ Illusory: Design for repetition with familiar phrases               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│  Output: misinfo_text + metadata                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 3: BELIEF ASSESSMENT (BEFORE)                                         │
│  belief_before = simulate_belief_before(misinfo_text, participant_id)       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Placeholder function simulates initial belief (0.6-0.9)             │    │
│  │ Adjusts based on misinformation characteristics                     │    │
│  │ • "everyone knows" → +0.1 belief                                    │    │
│  │ • "study shows" → +0.15 belief                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 4: GENERATE CORRECTION                                                │
│  Framework Y.generate_correction(misinfo_text, metadata, tone, cohort)      │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ ELM: Counter with central route (evidence, logic, citations)        │    │
│  │ FTT: Provide correct gist + detailed verbatim clarification         │    │
│  │ Schema: Affirm values, show misuse, give factual alternative        │    │
│  │ Illusory: Disrupt familiarity with novel facts, unusual wording     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│  Output: correction_text + correction_metadata                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 5: BELIEF ASSESSMENT (AFTER)                                          │
│  belief_after = simulate_belief_after(correction_text, belief_before, pid)  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Simulates correction effectiveness (reduction 0.1-0.6)              │    │
│  │ Adjusts based on correction characteristics                         │    │
│  │ • "evidence shows" → +0.1 reduction                                 │    │
│  │ • "studies demonstrate" → +0.15 reduction                           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│  Calculate effectiveness = belief_before - belief_after                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 6: LOG EXPERIMENT DATA                                                │
│  Save to data/outputs/corrections_log.csv                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ • timestamp, participant_id, cohort                                 │    │
│  │ • original_claim, misinfo_framework, correction_framework           │    │
│  │ • misinfo_text, correction_text                                     │    │
│  │ • belief_before, belief_after, effectiveness                        │    │
│  │ • All framework-specific metadata                                   │    │ 
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
                              BATCH EXPERIMENTS
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│  FOR EACH COMBINATION:                                                      │
│  • Multiple claims: ["claim1", "claim2", "claim3"]                          │
│  • Multiple participants: ["P001", "P002", "P003"]                          │
│  • Selected frameworks: ["elm_general", "ftt"]                              │
│                                                                             │
│  Loop through all combinations and run single experiment flow               │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
                               FULL MATRIX (X→Y)
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│  COMPLETE FRAMEWORK MATRIX (4×4 = 16 combinations):                         │
│                                                                             │
│  Misinformation (X) │ Correction (Y)     │ Test Status                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  elm_general        │ elm_general        │ ✓ ELM→ELM                       │
│  elm_general        │ ftt                │ ✓ ELM→FTT                       │
│  elm_general        │ schema_general     │ ✓ ELM→Schema                    │
│  elm_general        │ illusory_truth     │ ✓ ELM→Illusory                  │
│  ftt                │ elm_general        │ ✓ FTT→ELM                       │
│  ftt                │ ftt                │ ✓ FTT→FTT                       │
│  ftt                │ schema_general     │ ✓ FTT→Schema                    │
│  ftt                │ illusory_truth     │ ✓ FTT→Illusory                  │
│  schema_general     │ elm_general        │ ✓ Schema→ELM                    │
│  schema_general     │ ftt                │ ✓ Schema→FTT                    │
│  schema_general     │ schema_general     │ ✓ Schema→Schema                 │
│  schema_general     │ illusory_truth     │ ✓ Schema→Illusory               │
│  illusory_truth     │ elm_general        │ ✓ Illusory→ELM                  │
│  illusory_truth     │ ftt                │ ✓ Illusory→FTT                  │
│  illusory_truth     │ schema_general     │ ✓ Illusory→Schema               │
│  illusory_truth     │ illusory_truth     │ ✓ Illusory→Illusory             │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
                              PRACTICAL USAGE
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│  OPTION 1: Quick Demo                                                       │
│  python experiments/run_demo.py                                             │
│  • Runs sample experiments with different framework combinations            │
│  • Shows belief before/after simulation                                     │
│  • Generates summary statistics                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  OPTION 2: Custom Single Experiment                                         │
│  controller = MisinformationController()                                    │
│  result = controller.run_experiment(                                        │
│      claim="Hot water cures all viruses",                                   │
│      participant_id="P001",                                                 │
│      cohort="general",                                                      │
│      misinfo_framework="illusory_truth",                                    │
│      correction_framework="elm_general"                                     │
│  )                                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  OPTION 3: Full Research Study                                              │
│  results = controller.run_full_matrix(                                      │
│      claims=["claim1", "claim2", "claim3"],                                 │
│      participant_ids=["P001", "P002", "P003"],                              │
│      cohort="general"                                                       │
│  )                                                                          │
│  # Generates 3 claims × 3 participants × 16 combinations = 144 experiments  │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
                                OUTPUT DATA
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│  EXPERIMENT RESULTS (corrections_log.csv):                                  │
│  • Comprehensive data for each experiment run                               │
│  • Framework-specific metadata for analysis                                 │
│  • Belief measurements for effectiveness calculation                        │
│  • Ready for statistical analysis and visualization                         │
│                                                                             │
│  RESEARCH QUESTIONS ANSWERABLE:                                             │
│  • Which correction framework is most effective overall?                    │
│  • Does framework matching (X→X) work better than cross-framework (X→Y)?    │
│  • Which misinformation types are hardest to correct?                       │
│  • How do different psychological approaches compare?                       │
└─────────────────────────────────────────────────────────────────────────────┘
```