"""Simple training script for all psychological framework classifiers."""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import load_training_data
from src.classifier import MisinformationClassifier
from src.config import Config

# Train all three framework classifiers
frameworks = ['elm', 'schema', 'fuzzy_trace']

for framework in frameworks:
    print(f"Training {framework} classifier...")
    
    try:
        train_dataset, val_dataset, test_dataset = load_training_data(framework)
        classifier = MisinformationClassifier(framework=framework)
        trainer = classifier.train(train_dataset, val_dataset)
        
        model_path = Config.PROJECT_ROOT / "models" / f"{framework}_classifier"
        model_path.mkdir(parents=True, exist_ok=True)
        classifier.save_model(str(model_path))
        print(f"{framework} model saved to {model_path}")
        
    except FileNotFoundError as e:
        print(f"Error training {framework}: {e}")
        print(f"Please place {framework}_data.csv in data/raw/ directory")

print("Training complete for all frameworks!")