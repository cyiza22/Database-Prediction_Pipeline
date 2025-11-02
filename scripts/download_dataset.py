import kagglehub
import pandas as pd
import os
import shutil

def download_telco_dataset():
    """
    Download the Telco Customer Churn dataset from Kaggle
    """
    try:
        # Download the dataset
        print("Downloading Telco Customer Churn dataset from Kaggle...")
        path = kagglehub.dataset_download("blastchar/telco-customer-churn")
        print(f"Dataset downloaded to: {path}")
        
        # Find the CSV file
        csv_file = None
        for file in os.listdir(path):
            if file.endswith('.csv'):
                csv_file = os.path.join(path, file)
                break
        
        if csv_file:
            # Copy to current directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            destination = os.path.join(current_dir, "Telco-Customer-Churn.csv")
            shutil.copy2(csv_file, destination)
            print(f"Dataset copied to: {destination}")
            
            # Load and display basic info
            df = pd.read_csv(destination)
            print(f"\nDataset loaded successfully!")
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print(f"\nFirst few rows:")
            print(df.head())
            
            return destination
        else:
            print("CSV file not found in downloaded dataset")
            return None
            
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return None

if __name__ == "__main__":
    download_telco_dataset()
