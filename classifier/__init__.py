"""Misinformation classification system."""

from .config import Config
from .data_loader import load_csv_data, load_jsonl_data, load_training_data
from .classifier import MisinformationClassifier
from .multi_framework_classifier import MultiFrameworkClassifier
from .evaluation import calculate_metrics, evaluate_model_performance

__version__ = "0.1.0"
__all__ = [
    "Config",
    "load_csv_data",
    "load_jsonl_data", 
    "load_training_data",
    "MisinformationClassifier",
    "MultiFrameworkClassifier",
    "calculate_metrics",
    "evaluate_model_performance"
]