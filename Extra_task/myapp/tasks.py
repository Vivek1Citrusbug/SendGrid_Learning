import pandas as pd
import json
from celery import shared_task



## extra task is not completed yet but will continue this whenever time permits.

@shared_task
def validate_data(file_path: str) -> str:
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Validation logic
    if df.isnull().any().any():
        raise ValueError("Dataset contains missing values.")
    if not pd.api.types.is_numeric_dtype(df["Quantity"]) or not pd.api.types.is_numeric_dtype(df["Price"]):
        raise ValueError("Quantity and Price columns must be numeric.")
    
    return file_path  # Pass the path to the next task

@shared_task
def transform_data(file_path: str) -> str:
    # Transform the dataset to JSON
    df = pd.read_csv(file_path)
    transformed_data = df.to_dict(orient="records")
    
    # Save as JSON
    transformed_file = file_path.replace(".csv", "_transformed.json")
    with open(transformed_file, "w") as f:
        json.dump(transformed_data, f)
    
    return transformed_file

@shared_task
def analyze_data(json_file_path: str) -> str:
    with open(json_file_path, "r") as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    summary = {
        "total_revenue_per_product": df.groupby("Product")["Price"].sum().to_dict(),
        "price_summary": {
            "mean": df["Price"].mean(),
            "median": df["Price"].median(),
            "mode": df["Price"].mode().tolist(),
        },
        "product_categories":df['Product'].unique()
    }
    
    # Save the analysis
    analysis_file = json_file_path.replace("_transformed.json", "_analysis.json")
    with open(analysis_file, "w") as f:
        json.dump(summary, f)
    
    return analysis_file

@shared_task
def generate_report(analysis_file: str) -> str:
    # Load analysis
    with open(analysis_file, "r") as f:
        analysis_data = json.load(f)
    
    # Create a summary report
    report_file = analysis_file.replace("_analysis.json", "_report.txt")
    with open(report_file, "w") as f:
        f.write("Data Analysis Report\n")
        f.write(json.dumps(analysis_data, indent=4))
    
    return report_file
