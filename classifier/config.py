"""Configuration settings for the misinformation classification system."""

import os
from pathlib import Path

class Config:
    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    SYNTHETIC_DATA_DIR = DATA_DIR / "synthetic"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    
    # Model configuration
    MODEL_NAME = "distilbert-base-uncased"
    MAX_LENGTH = 512
    
    # Training hyperparameters
    BATCH_SIZE = 16
    LEARNING_RATE = 2e-5
    NUM_EPOCHS = 3
    WARMUP_STEPS = 500
    WEIGHT_DECAY = 0.01
    
    # Evaluation settings
    CV_FOLDS = 5
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    
    # Psychological Framework Configurations
    FRAMEWORKS = {
        "elm": {
            "name": "Elaboration Likelihood Model",
            "labels": ["central", "peripheral"],
            "num_labels": 2,
            "description": "Central (logical/evidence) vs Peripheral (emotional/superficial) processing"
        },
        "schema": {
            "name": "Schema Theory", 
            "labels": ["congruent", "incongruent"],
            "num_labels": 2,
            "description": "Schema-congruent vs schema-incongruent information processing"
        },
        "fuzzy_trace": {
            "name": "Fuzzy Trace Theory",
            "labels": ["no_distortion", "gist_distortion"],
            "num_labels": 2,
            "description": "Gist-verbatim distortion detection"
        }
    }
    
    # Default framework for training
    DEFAULT_FRAMEWORK = "elm"