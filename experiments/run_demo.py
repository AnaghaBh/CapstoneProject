import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from controller import MisinformationController

def run_demo():
    """Run hybrid architecture demo with full X-Y framework matrix."""
    
    controller = MisinformationController()
    
    print("=== Hybrid Misinformation Architecture Demo ===")
    print("Testing: Framework X (Misinformation) → Framework Y (Correction)\n")
    
    # Sample claims for testing
    sample_claims = [
        "Drinking hot water cures all viruses instantly",
        "Vaccines contain dangerous microchips",
        "Climate change is completely fake"
    ]
    
    # Sample participant IDs
    participant_ids = ["P001", "P002"]
    
    print("Running individual experiments:")
    print("-" * 60)
    
    results = []
    
    # Run a few individual experiments
    for i, claim in enumerate(sample_claims[:2]):
        print(f"\nExperiment {i+1}: {claim}")
        
        try:
            result = controller.run_experiment(
                claim=claim,
                participant_id=f"P00{i+1}",
                cohort="general"
            )
            
            results.append({
                'misinfo_framework': result['misinfo_framework'],
                'correction_framework': result['correction_framework'],
                'belief_before': result['belief_before'],
                'belief_after': result['belief_after'],
                'effectiveness': result['effectiveness']
            })
            
            print(f"  {result['misinfo_framework']} → {result['correction_framework']}")
            print(f"  Belief: {result['belief_before']:.2f} → {result['belief_after']:.2f}")
            print(f"  Effectiveness: {result['effectiveness']:.2f}")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    print(f"\n{'='*60}")
    print("FRAMEWORK MATRIX DEMO")
    print(f"{'='*60}")
    
    # Demonstrate matrix capabilities
    frameworks = list(controller.frameworks.keys())
    
    print("\nFramework Combinations Matrix:")
    print(f"{'Misinformation':<15} {'Correction':<15} {'Status'}")
    print("-" * 45)
    
    for misinfo_fw in frameworks:
        for correction_fw in frameworks:
            try:
                # Quick test
                test_result = controller.run_experiment(
                    claim="Test claim for matrix",
                    participant_id="TEST",
                    cohort="general",
                    misinfo_framework=misinfo_fw,
                    correction_framework=correction_fw
                )
                status = "✓ Working"
            except Exception as e:
                status = f"✗ Error: {str(e)[:20]}..."
            
            print(f"{misinfo_fw:<15} {correction_fw:<15} {status}")
    
    # Summary statistics
    if results:
        print(f"\n{'='*60}")
        print("SUMMARY STATISTICS")
        print(f"{'='*60}")
        
        df = pd.DataFrame(results)
        print(f"\nAverage effectiveness by framework:")
        
        misinfo_avg = df.groupby('misinfo_framework')['effectiveness'].mean()
        correction_avg = df.groupby('correction_framework')['effectiveness'].mean()
        
        print("\nMisinformation Framework Performance:")
        for fw, eff in misinfo_avg.items():
            print(f"  {fw}: {eff:.2f}")
        
        print("\nCorrection Framework Performance:")
        for fw, eff in correction_avg.items():
            print(f"  {fw}: {eff:.2f}")
        
        # Save results
        df.to_csv("data/outputs/demo_results.csv", index=False)
        print(f"\nResults saved to: data/outputs/demo_results.csv")
    
    print(f"\n{'='*60}")
    print("Demo completed! Full experiment logs in corrections_log.csv")
    print("Use controller.run_full_matrix() for complete X-Y testing.")

if __name__ == "__main__":
    run_demo()