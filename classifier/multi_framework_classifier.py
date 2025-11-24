"""Multi-framework classifier for analyzing psychological frameworks in text."""

import torch
import numpy as np
from typing import Dict, List, Tuple
from .classifier import MisinformationClassifier
from .config import Config

class MultiFrameworkClassifier:
    """Classifier that analyzes text across all psychological frameworks."""
    
    def __init__(self):
        """Initialize classifiers for all frameworks."""
        self.classifiers = {}
        self.frameworks = list(Config.FRAMEWORKS.keys())
        
        # Load trained models for each framework
        for framework in self.frameworks:
            try:
                classifier = MisinformationClassifier(framework=framework)
                model_path = Config.PROJECT_ROOT / "models" / f"{framework}_classifier"
                classifier.load_model(str(model_path))
                self.classifiers[framework] = classifier
                print(f"Loaded {framework} classifier")
            except Exception as e:
                print(f"Warning: Could not load {framework} classifier: {e}")
    
    def analyze_text(self, text: str) -> Dict[str, Dict[str, float]]:
        """Analyze text across all frameworks and return confidence scores.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with framework predictions and confidence scores
        """
        results = {}
        
        for framework_name, classifier in self.classifiers.items():
            framework_config = Config.FRAMEWORKS[framework_name]
            
            # Get prediction probabilities
            inputs = classifier.tokenizer(
                text,
                truncation=True,
                padding=True,
                max_length=Config.MAX_LENGTH,
                return_tensors="pt"
            )
            
            with torch.no_grad():
                outputs = classifier.model(**inputs)
                probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
                probs = probabilities[0].numpy()
            
            # Map probabilities to labels
            framework_results = {}
            for i, label in enumerate(framework_config["labels"]):
                framework_results[label] = float(probs[i])
            
            results[framework_name] = framework_results
        
        return results
    
    def get_framework_confidence(self, text: str) -> Dict[str, float]:
        """Get overall confidence that each framework applies to the text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with framework names and confidence percentages
        """
        analysis = self.analyze_text(text)
        framework_confidence = {}
        
        for framework_name, predictions in analysis.items():
            # For binary classification, use the positive class probability
            if framework_name == "elm":
                # Higher confidence if it's peripheral processing (emotional/superficial)
                confidence = predictions.get("peripheral", 0.0)
            elif framework_name == "schema":
                # Higher confidence if it's incongruent (conflicts with beliefs)
                confidence = predictions.get("incongruent", 0.0)
            elif framework_name == "fuzzy_trace":
                # Higher confidence if there's gist distortion
                confidence = predictions.get("gist_distortion", 0.0)
            else:
                # Default: use maximum probability
                confidence = max(predictions.values())
            
            framework_confidence[framework_name] = confidence * 100
        
        return framework_confidence
    
    def classify_text(self, text: str, threshold: float = 0.5) -> Dict:
        """Classify text and return detailed analysis.
        
        Args:
            text: Input text to analyze
            threshold: Minimum confidence threshold for framework detection
            
        Returns:
            Comprehensive analysis results
        """
        detailed_analysis = self.analyze_text(text)
        framework_confidence = self.get_framework_confidence(text)
        
        # Determine active frameworks
        active_frameworks = {
            framework: confidence 
            for framework, confidence in framework_confidence.items()
            if confidence >= threshold * 100
        }
        
        return {
            "text": text,
            "framework_confidence": framework_confidence,
            "active_frameworks": active_frameworks,
            "detailed_analysis": detailed_analysis,
            "summary": self._generate_summary(framework_confidence, active_frameworks)
        }
    
    def _generate_summary(self, confidence: Dict[str, float], active: Dict[str, float]) -> str:
        """Generate human-readable summary of the analysis."""
        if not active:
            return "No psychological frameworks detected above threshold."
        
        # Sort by confidence
        sorted_frameworks = sorted(active.items(), key=lambda x: x[1], reverse=True)
        
        summary_parts = []
        for framework, conf in sorted_frameworks:
            framework_name = Config.FRAMEWORKS[framework]["name"]
            summary_parts.append(f"{framework_name}: {conf:.1f}%")
        
        return "Detected frameworks: " + ", ".join(summary_parts)