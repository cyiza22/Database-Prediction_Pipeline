import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

# Load dataset (after downloading with kagglehub)
df = pd.read_csv("Telco-Customer-Churn.csv")

# Create collections
customers_col = db["customers"]
contracts_col = db["contracts"]
services_col = db["services"]

# Split and insert relevant data
customer_fields = ['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService']
contract_fields = ['customerID', 'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Churn']
service_fields = ['customerID', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']

customers_col.insert_many(df[customer_fields].to_dict("records"))
contracts_col.insert_many(df[contract_fields].to_dict("records"))
services_col.insert_many(df[service_fields].to_dict("records"))

print("MongoDB collections created and populated successfully.")
