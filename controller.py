import random
import pandas as pd
from datetime import datetime
from modules import elm_general, ftt, schema_general, illusory_truth
from utils.logging_utils import log_experiment

class MisinformationController:
    """Central controller for misinformation generation and correction experiments."""
    
    def __init__(self):
        self.frameworks = {
            'elm_general': elm_general,
            'ftt': ftt,
            'schema_general': schema_general,
            'illusory_truth': illusory_truth
        }
    
    def run_experiment(self, claim, participant_id, cohort, misinfo_framework=None, correction_framework=None):
        """Run complete misinformation-correction experiment."""
        
        # Select frameworks
        if not misinfo_framework:
            misinfo_framework = random.choice(list(self.frameworks.keys()))
        if not correction_framework:
            correction_framework = random.choice(list(self.frameworks.keys()))
        
        print(f"Experiment: {misinfo_framework} → {correction_framework}")
        
        # Get framework modules
        misinfo_module = self.frameworks[misinfo_framework]
        correction_module = self.frameworks[correction_framework]
        
        # Step 1: Analyze original claim
        original_metadata = misinfo_module.analyse_claim(claim)
        
        # Step 2: Generate misinformation using framework X
        misinfo_params = self._get_default_params(misinfo_framework)
        misinfo_text, misinfo_metadata = misinfo_module.simulate_misinformation(misinfo_params)
        
        # Step 3: Simulate belief_before (placeholder)
        belief_before = self._simulate_belief_before(misinfo_text, participant_id)
        
        # Step 4: Generate correction using framework Y
        correction_text, correction_metadata = correction_module.generate_correction(
            misinfo_text, misinfo_metadata, tone="neutral", cohort=cohort
        )
        
        # Step 5: Simulate belief_after (placeholder)
        belief_after = self._simulate_belief_after(correction_text, belief_before, participant_id)
        
        # Step 6: Log everything
        experiment_data = {
            'timestamp': datetime.now().isoformat(),
            'participant_id': participant_id,
            'cohort': cohort,
            'original_claim': claim,
            'misinfo_framework': misinfo_framework,
            'correction_framework': correction_framework,
            'misinfo_text': misinfo_text,
            'correction_text': correction_text,
            'belief_before': belief_before,
            'belief_after': belief_after,
            'effectiveness': belief_before - belief_after,
            **original_metadata,
            **misinfo_metadata,
            **correction_metadata
        }
        
        log_experiment(experiment_data, "data/outputs/corrections_log.csv")
        
        return experiment_data
    
    def run_full_matrix(self, claims, participant_ids, cohort="general"):
        """Run full X-Y framework matrix experiment."""
        results = []
        
        for claim in claims:
            for participant_id in participant_ids:
                for misinfo_fw in self.frameworks.keys():
                    for correction_fw in self.frameworks.keys():
                        try:
                            result = self.run_experiment(
                                claim, participant_id, cohort, misinfo_fw, correction_fw
                            )
                            results.append(result)
                        except Exception as e:
                            print(f"Error in {misinfo_fw}→{correction_fw}: {e}")
        
        return pd.DataFrame(results)
    
    def _get_default_params(self, framework):
        """Get default parameters for framework simulation."""
        defaults = {
            'elm_general': {'route': 'peripheral'},
            'ftt': {'topic': 'health'},
            'schema_general': {'schema_category': 'health_safety'},
            'illusory_truth': {'repetition_level': 'high'}
        }
        return defaults.get(framework, {})
    
    def _simulate_belief_before(self, misinfo_text, participant_id):
        """Placeholder for belief assessment before correction."""
        # Simulate based on misinformation characteristics
        base_belief = random.uniform(0.6, 0.9)
        if "everyone knows" in misinfo_text.lower():
            base_belief += 0.1
        if "study shows" in misinfo_text.lower():
            base_belief += 0.15
        return min(base_belief, 1.0)
    
    def _simulate_belief_after(self, correction_text, belief_before, participant_id):
        """Placeholder for belief assessment after correction."""
        # Simulate correction effectiveness
        reduction = random.uniform(0.1, 0.6)
        if "evidence shows" in correction_text.lower():
            reduction += 0.1
        if "studies demonstrate" in correction_text.lower():
            reduction += 0.15
        return max(belief_before - reduction, 0.0)

if __name__ == "__main__":
    controller = MisinformationController()
    
    # Test single experiment
    result = controller.run_experiment(
        claim="Drinking hot water cures viruses",
        participant_id="P001",
        cohort="general"
    )
    
    print("Experiment Result:")
    for key, value in result.items():
        if isinstance(value, str) and len(value) > 100:
            print(f"{key}: {value[:100]}...")
        else:
            print(f"{key}: {value}")