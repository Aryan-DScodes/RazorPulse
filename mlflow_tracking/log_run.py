# In a real environment, you would run 'pip install mlflow' 
# and use the actual library. This is our interface stub.

def log_experiment(run_name: str, params: dict, metrics: dict, artifacts: list):
    """
    Logs the evaluation run to MLflow.
    """
    print(f"--- MLflow Run: {run_name} ---")
    print("Params:")
    for k, v in params.items():
        print(f"  {k}: {v}")
        
    print("Metrics:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
        
    print(f"Artifacts saved: {len(artifacts)} files")
    print("-----------------------------------")