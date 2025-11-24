"""Evaluation utilities for the misinformation classification system."""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, 
    f1_score, 
    precision_score, 
    recall_score,
    confusion_matrix,
    classification_report
)
from sklearn.model_selection import cross_val_score, StratifiedKFold
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Tuple
from .config import Config

def calculate_metrics(y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
    """Calculate classification metrics."""
    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'f1_macro': f1_score(y_true, y_pred, average='macro'),
        'f1_weighted': f1_score(y_true, y_pred, average='weighted'),
        'precision_macro': precision_score(y_true, y_pred, average='macro'),
        'recall_macro': recall_score(y_true, y_pred, average='macro')
    }

def plot_confusion_matrix(y_true: List[int], y_pred: List[int], 
                         labels: List[str] = None, save_path: str = None) -> None:
    """Plot confusion matrix."""
    if labels is None:
        labels = Config.FRAMEWORK_LABELS
    
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def generate_classification_report(y_true: List[int], y_pred: List[int], 
                                 labels: List[str] = None) -> str:
    """Generate detailed classification report."""
    if labels is None:
        labels = Config.FRAMEWORK_LABELS
    
    return classification_report(y_true, y_pred, target_names=labels)

def cross_validate_model(model, X: np.ndarray, y: np.ndarray, 
                        cv_folds: int = None) -> Dict[str, Any]:
    """Perform cross-validation on the model."""
    if cv_folds is None:
        cv_folds = Config.CV_FOLDS
    
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=Config.RANDOM_STATE)
    
    # Calculate cross-validation scores for different metrics
    accuracy_scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    f1_scores = cross_val_score(model, X, y, cv=cv, scoring='f1_macro')
    
    return {
        'accuracy_mean': accuracy_scores.mean(),
        'accuracy_std': accuracy_scores.std(),
        'f1_mean': f1_scores.mean(),
        'f1_std': f1_scores.std(),
        'accuracy_scores': accuracy_scores.tolist(),
        'f1_scores': f1_scores.tolist()
    }

def evaluate_model_performance(y_true: List[int], y_pred: List[int], 
                             labels: List[str] = None) -> Dict[str, Any]:
    """Comprehensive model evaluation."""
    if labels is None:
        labels = Config.FRAMEWORK_LABELS
    
    metrics = calculate_metrics(y_true, y_pred)
    report = generate_classification_report(y_true, y_pred, labels)
    
    return {
        'metrics': metrics,
        'classification_report': report,
        'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
    }

def compare_models(results: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """Compare performance of multiple models."""
    comparison_data = []
    
    for model_name, model_results in results.items():
        metrics = model_results['metrics']
        comparison_data.append({
            'Model': model_name,
            'Accuracy': metrics['accuracy'],
            'F1 (Macro)': metrics['f1_macro'],
            'F1 (Weighted)': metrics['f1_weighted'],
            'Precision (Macro)': metrics['precision_macro'],
            'Recall (Macro)': metrics['recall_macro']
        })
    
    return pd.DataFrame(comparison_data)

def save_evaluation_results(results: Dict[str, Any], output_path: str) -> None:
    """Save evaluation results to file."""
    import json
    
    # Convert numpy arrays to lists for JSON serialization
    serializable_results = {}
    for key, value in results.items():
        if isinstance(value, np.ndarray):
            serializable_results[key] = value.tolist()
        else:
            serializable_results[key] = value
    
    with open(output_path, 'w') as f:
        json.dump(serializable_results, f, indent=2)