import pandas as pd
import os

def log_output(timestamp, claim, framework, cohort, correction, log_path):
    """Log correction output to CSV file."""
    data = {
        'timestamp': [timestamp],
        'claim': [claim],
        'framework': [framework],
        'cohort': [cohort],
        'correction': [correction]
    }
    
    df = pd.DataFrame(data)
    
    if os.path.exists(log_path):
        df.to_csv(log_path, mode='a', header=False, index=False)
    else:
        df.to_csv(log_path, index=False)

def log_experiment(experiment_data, log_path):
    """Log complete experiment data to CSV file."""
    df = pd.DataFrame([experiment_data])
    
    if os.path.exists(log_path):
        df.to_csv(log_path, mode='a', header=False, index=False)
    else:
        df.to_csv(log_path, index=False)