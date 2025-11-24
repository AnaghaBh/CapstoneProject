"""Data loading utilities for the misinformation classification system."""

import pandas as pd
import json
from pathlib import Path
from typing import Tuple, List, Dict, Any
from sklearn.model_selection import train_test_split
from datasets import Dataset
from .config import Config

def load_csv_data(file_path: Path) -> pd.DataFrame:
    """Load data from CSV file."""
    return pd.read_csv(file_path)

def load_jsonl_data(file_path: Path) -> List[Dict[str, Any]]:
    """Load data from JSONL file."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

def prepare_dataset(texts: List[str], labels: List[str], framework: str = None) -> Dataset:
    """Convert texts and labels to Hugging Face Dataset format."""
    framework = framework or Config.DEFAULT_FRAMEWORK
    framework_labels = Config.FRAMEWORKS[framework]["labels"]
    label_to_id = {label: idx for idx, label in enumerate(framework_labels)}
    label_ids = [label_to_id[label] for label in labels]
    
    return Dataset.from_dict({
        'text': texts,
        'labels': label_ids
    })

def split_data(texts: List[str], labels: List[str], framework: str = None) -> Tuple[Dataset, Dataset, Dataset]:
    """Split data into train, validation, and test sets."""
    # First split: separate test set
    X_temp, X_test, y_temp, y_test = train_test_split(
        texts, labels, 
        test_size=Config.TEST_SIZE, 
        random_state=Config.RANDOM_STATE,
        stratify=labels
    )
    
    # Second split: separate train and validation
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp,
        test_size=0.25,  # 0.25 * 0.8 = 0.2 of total data
        random_state=Config.RANDOM_STATE,
        stratify=y_temp
    )
    
    train_dataset = prepare_dataset(X_train, y_train, framework)
    val_dataset = prepare_dataset(X_val, y_val, framework)
    test_dataset = prepare_dataset(X_test, y_test, framework)
    
    return train_dataset, val_dataset, test_dataset

def load_training_data(framework: str = None, data_file: str = None) -> Tuple[Dataset, Dataset, Dataset]:
    """Load and prepare training data from configured paths.
    
    Args:
        framework: Psychological framework to load data for
        data_file: Specific data file to load (optional)
    """
    framework = framework or Config.DEFAULT_FRAMEWORK
    
    # Load data from raw directory
    if data_file:
        file_path = Config.RAW_DATA_DIR / data_file
    else:
        # Look for framework-specific files
        file_path = Config.RAW_DATA_DIR / f"{framework}_data.csv"
        if not file_path.exists():
            file_path = Config.RAW_DATA_DIR / "data.csv"
    
    if not file_path.exists():
        raise FileNotFoundError(f"No data file found at {file_path}")
    
    # Load and process data based on file extension
    if file_path.suffix == '.csv':
        df = load_csv_data(file_path)
        texts = df['text'].tolist()
        labels = df['label'].tolist()
    elif file_path.suffix == '.jsonl':
        data = load_jsonl_data(file_path)
        texts = [item['text'] for item in data]
        labels = [item['label'] for item in data]
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    return split_data(texts, labels, framework)