import pandas as pd
import psycopg2
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import numpy as np

# Load environment variables
load_dotenv()

def setup_postgresql():
    """
    Set up PostgreSQL database with schema and data
    """
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=os.getenv("PG_DB"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT")
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Connected to PostgreSQL!")
        
        # Read and execute schema
        sql_dir = os.path.join(os.path.dirname(__file__), '..', 'sql')
        schema_file = os.path.join(sql_dir, 'schema_design.sql')
        
        with open(schema_file, 'r') as file:
            schema_sql = file.read()
        
        # Split by statements and execute
        statements = schema_sql.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    print(f"Executed: {statement[:50]}...")
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        print(f"Error executing statement: {e}")
        
        # Load dataset and insert data
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        csv_file = None
        
        # Find the CSV file
        for file in os.listdir(data_dir):
            if file.endswith('.csv') and 'telco' in file.lower():
                csv_file = os.path.join(data_dir, file)
                break
        
        if csv_file and os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            
            # Clean data
            df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
            df = df.dropna()
            
            # Insert customers data
            print("Inserting customers data...")
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO customers (customer_name, gender, senior_citizen, partner, dependents, tenure, phone_service)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING customer_id
                """, (
                    f"Customer_{row['customerID']}", 
                    row['gender'],
                    bool(row['SeniorCitizen']),
                    row['Partner'] == 'Yes',
                    row['Dependents'] == 'Yes',
                    int(row['tenure']),
                    row['PhoneService'] == 'Yes'
                ))
                customer_id = cursor.fetchone()[0]
                
                # Insert contracts data
                cursor.execute("""
                    INSERT INTO contracts (customer_id, contract_type, paperless_billing, payment_method, monthly_charges, total_charges, churn)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    customer_id,
                    row['Contract'],
                    row['PaperlessBilling'] == 'Yes',
                    row['PaymentMethod'],
                    float(row['MonthlyCharges']),
                    float(row['TotalCharges']),
                    row['Churn'] == 'Yes'
                ))
                
                # Insert services data
                cursor.execute("""
                    INSERT INTO services (customer_id, internet_service, online_security, online_backup, device_protection, tech_support, streaming_tv, streaming_movies)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    customer_id,
                    row['InternetService'],
                    row['OnlineSecurity'],
                    row['OnlineBackup'],
                    row['DeviceProtection'],
                    row['TechSupport'],
                    row['StreamingTV'],
                    row['StreamingMovies']
                ))
            
            print(f"Inserted {len(df)} records into PostgreSQL")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error setting up PostgreSQL: {e}")
        return False

def setup_mongodb():
    """
    Set up MongoDB collections with data
    """
    try:
        # Connect to MongoDB
        client = MongoClient(os.getenv("MONGO_URI"))
        db = client[os.getenv("MONGO_DB")]
        
        print("Connected to MongoDB!")
        
        # Clear existing collections
        db.customers.drop()
        db.contracts.drop()
        db.services.drop()
        
        # Load dataset
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        csv_file = None
        
        # Find the CSV file
        for file in os.listdir(data_dir):
            if file.endswith('.csv') and 'telco' in file.lower():
                csv_file = os.path.join(data_dir, file)
                break
        
        if csv_file and os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            
            # Clean data
            df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
            df = df.dropna()
            
            # Convert to MongoDB documents
            customers_data = []
            contracts_data = []
            services_data = []
            
            for _, row in df.iterrows():
                customer_id = row['customerID']
                
                # Customer document
                customers_data.append({
                    'customerID': customer_id,
                    'customer_name': f"Customer_{customer_id}",
                    'gender': row['gender'],
                    'SeniorCitizen': bool(row['SeniorCitizen']),
                    'Partner': row['Partner'] == 'Yes',
                    'Dependents': row['Dependents'] == 'Yes',
                    'tenure': int(row['tenure']),
                    'PhoneService': row['PhoneService'] == 'Yes'
                })
                
                # Contract document
                contracts_data.append({
                    'customerID': customer_id,
                    'Contract': row['Contract'],
                    'PaperlessBilling': row['PaperlessBilling'] == 'Yes',
                    'PaymentMethod': row['PaymentMethod'],
                    'MonthlyCharges': float(row['MonthlyCharges']),
                    'TotalCharges': float(row['TotalCharges']),
                    'Churn': row['Churn'] == 'Yes'
                })
                
                # Services document
                services_data.append({
                    'customerID': customer_id,
                    'InternetService': row['InternetService'],
                    'OnlineSecurity': row['OnlineSecurity'],
                    'OnlineBackup': row['OnlineBackup'],
                    'DeviceProtection': row['DeviceProtection'],
                    'TechSupport': row['TechSupport'],
                    'StreamingTV': row['StreamingTV'],
                    'StreamingMovies': row['StreamingMovies']
                })
            
            # Insert into collections
            db.customers.insert_many(customers_data)
            db.contracts.insert_many(contracts_data)
            db.services.insert_many(services_data)
            
            print(f"Inserted {len(df)} records into MongoDB collections")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"Error setting up MongoDB: {e}")
        return False

def main():
    """
    Main setup function
    """
    print("Setting up databases...")
    
    # Check if dataset exists
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    csv_exists = False
    
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith('.csv') and 'telco' in file.lower():
                csv_exists = True
                break
    
    if not csv_exists:
        print("Dataset not found. Please run scripts/download_dataset.py first.")
        return
    
    # Setup PostgreSQL
    if setup_postgresql():
        print("✅ PostgreSQL setup completed successfully!")
    else:
        print("❌ PostgreSQL setup failed!")
    
    # Setup MongoDB
    if setup_mongodb():
        print("✅ MongoDB setup completed successfully!")
    else:
        print("❌ MongoDB setup failed!")

if __name__ == "__main__":
    main()
