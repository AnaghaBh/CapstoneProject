# Psychological Misinformation Framework Classification System

A machine learning system for analyzing misinformation content according to psychological processing frameworks using DistilBERT. The system can analyze text across multiple frameworks simultaneously and provide confidence percentages for each framework.

## Project Purpose

This project builds classifiers that identify how misinformation is processed cognitively based on established psychological frameworks. The system analyzes text and provides confidence scores showing which psychological processing patterns are present (e.g., "30% Fuzzy Trace Theory, 70% Elaboration Likelihood Model").

## Psychological Frameworks

The system classifies content according to three psychological frameworks:

### 1. Elaboration Likelihood Model (ELM)
Classifies information processing routes:
- **Central Processing** - Logical, evidence-based reasoning
- **Peripheral Processing** - Emotional, superficial cues

### 2. Schema Theory  
Classifies schema congruence:
- **Schema Congruent** - Information aligns with existing beliefs
- **Schema Incongruent** - Information conflicts with existing beliefs

### 3. Fuzzy Trace Theory
Detects gist-verbatim distortions:
- **No Distortion** - Gist matches detailed information
- **Gist Distortion** - Gist misrepresents or exaggerates details

## Project Structure

```
misinformation-classifier/
├── src/                              # Source code modules
│   ├── config.py                     # Configuration settings
│   ├── data_loader.py                # Data loading utilities
│   ├── classifier.py                 # DistilBERT classifier implementation
│   ├── multi_framework_classifier.py # Multi-framework analysis
│   └── evaluation.py                 # Model evaluation utilities
├── scripts/                          # Execution scripts
│   ├── train_classifier.py           # Train all framework models
│   └── analyze_text.py               # Analyze text across all frameworks
├── data/                             # Data directories
│   ├── raw/                          # Original datasets
│   └── processed/                    # Cleaned and processed data
├── models/                           # Trained model storage
│   ├── elm_classifier/               # ELM framework model
│   ├── schema_classifier/            # Schema Theory model
│   └── fuzzy_trace_classifier/       # Fuzzy Trace Theory model
└── requirements.txt                  # Python dependencies
```

## Workflow

1. **Data Preparation**: Place annotated data files in the data/raw/ directory
2. **Model Training**: Train separate DistilBERT models for each psychological framework
3. **Multi-Framework Analysis**: Analyze text across all frameworks simultaneously
4. **Evaluation**: Assess model performance and framework detection accuracy
5. **Deployment**: Use trained models for real-time psychological framework analysis

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Data Placement**:
   - Place raw datasets (CSV or JSONL format) in `data/raw/`
   - Ensure data files have columns: `text` (content) and `label` (framework category)
   - Supported formats:
     - CSV: `text,label` columns
     - JSONL: `{"text": "content", "label": "category"}` per line

3. **Configuration**:
   - Modify `src/config.py` to adjust model parameters, paths, and hyperparameters
   - Update framework labels if using different categories

## Usage

### 1. Train All Framework Models

```bash
# Train all framework classifiers at once
python scripts/train_classifier.py
```

### 2. Analyze Text Across All Frameworks

```bash
# Simple analysis with confidence percentages
python scripts/analyze_text.py --text "Everyone knows vaccines are dangerous!"

# Detailed analysis showing all probabilities
python scripts/analyze_text.py --text "Studies show climate change causes floods" --output detailed

# JSON output for programmatic use
python scripts/analyze_text.py --text "Your headline here" --output json --threshold 0.3
```

**Example Output:**
```
Framework Confidence:
  Elaboration Likelihood Model: 85.2%
  Schema Theory: 45.1%
  Fuzzy Trace Theory: 12.3%

Detected frameworks: Elaboration Likelihood Model: 85.2%
```



## Multi-Framework Analysis

The system's key feature is analyzing text across all psychological frameworks simultaneously:

### Analysis Options

- **Simple**: Shows framework confidence percentages
- **Detailed**: Shows individual label probabilities within each framework
- **JSON**: Machine-readable output for integration
- **Threshold**: Set minimum confidence for framework detection (default: 50%)

### Use Cases

1. **Content Analysis**: Determine which psychological processing patterns are present in misinformation
2. **Research**: Study how different frameworks apply to the same content
3. **Detection**: Identify texts that strongly exhibit specific psychological patterns
4. **Comparison**: Compare framework activation across different types of content

## Model Configuration

Key configuration options in `src/config.py`:

- **Model**: DistilBERT base (uncased)
- **Max Sequence Length**: 512 tokens
- **Batch Size**: 16
- **Learning Rate**: 2e-5
- **Training Epochs**: 3
- **Cross-validation Folds**: 5

## Data Requirements

### Input Format

The system expects text data with corresponding psychological framework labels:

**ELM Framework (elm_data.csv)**:
```csv
text,label
"According to Oxford study, masks reduce transmission by 70%",central
"Everyone knows masks don't work, just look around!",peripheral
```

**Schema Theory (schema_data.csv)**:
```csv
text,label
"Raising minimum wage reduces inequality",congruent
"Healthcare should be accessible to all",incongruent
```

**Fuzzy Trace Theory (fuzzy_trace_data.csv)**:
```csv
text,label
"Climate change accelerates sea-level rise",no_distortion
"Study finds vaccine causes heart inflammation",gist_distortion
```

### Framework Labels

- **ELM**: `central`, `peripheral`
- **Schema Theory**: `congruent`, `incongruent`  
- **Fuzzy Trace Theory**: `no_distortion`, `gist_distortion`

## Evaluation Metrics

The system provides comprehensive evaluation including:

- **Accuracy**: Overall classification accuracy
- **F1 Score**: Macro and weighted F1 scores
- **Precision/Recall**: Per-class and macro-averaged
- **Confusion Matrix**: Visual representation of classification results
- **Cross-validation**: K-fold validation for robust performance assessment

## Contributing

When adding new data or modifying the system:

1. Place new raw data files in `data/raw/`
2. Update configuration in `src/config.py` if needed
3. Run data exploration in the provided notebook
4. Retrain the model using the training script
5. Evaluate results and document performance

