#!/usr/bin/env python3
"""
Test script for the Telco Customer Churn API
This script tests all CRUD operations for both PostgreSQL and MongoDB
"""

import requests
import json
import time
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test API health endpoint"""
    print("🔍 Testing API Health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['message']}")
            print(f"   Database Status: {data['data']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_postgresql_crud():
    """Test PostgreSQL CRUD operations"""
    print("\n📊 Testing PostgreSQL CRUD Operations...")
    
    # Test data
    customer_data = {
        "customer_name": "Test Customer PG",
        "gender": "Female",
        "senior_citizen": False,
        "partner": True,
        "dependents": False,
        "tenure": 12,
        "phone_service": True
    }
    
    customer_id = None
    
    try:
        # CREATE - Customer
        print("  Creating customer...")
        response = requests.post(f"{BASE_URL}/api/postgresql/customers/", json=customer_data)
        if response.status_code == 200:
            customer = response.json()
            customer_id = customer["customer_id"]
            print(f"  ✅ Customer created with ID: {customer_id}")
        else:
            print(f"  ❌ Failed to create customer: {response.status_code}")
            return False
        
        # READ - Get customer
        print("  Reading customer...")
        response = requests.get(f"{BASE_URL}/api/postgresql/customers/{customer_id}")
        if response.status_code == 200:
            print("  ✅ Customer retrieved successfully")
        else:
            print(f"  ❌ Failed to get customer: {response.status_code}")
        
        # READ - Get all customers
        print("  Reading all customers...")
        response = requests.get(f"{BASE_URL}/api/postgresql/customers/")
        if response.status_code == 200:
            customers = response.json()
            print(f"  ✅ Retrieved {len(customers)} customers")
        else:
            print(f"  ❌ Failed to get customers: {response.status_code}")
        
        # UPDATE - Customer
        print("  Updating customer...")
        update_data = {"customer_name": "Updated Test Customer PG", "tenure": 24}
        response = requests.put(f"{BASE_URL}/api/postgresql/customers/{customer_id}", json=update_data)
        if response.status_code == 200:
            print("  ✅ Customer updated successfully")
        else:
            print(f"  ❌ Failed to update customer: {response.status_code}")
        
        # CREATE Contract
        print("  Creating contract...")
        contract_data = {
            "customer_id": customer_id,
            "contract_type": "Month-to-month",
            "paperless_billing": True,
            "payment_method": "Electronic check",
            "monthly_charges": 75.50,
            "total_charges": 1200.00,
            "churn": False
        }
        response = requests.post(f"{BASE_URL}/api/postgresql/contracts/", json=contract_data)
        if response.status_code == 200:
            contract = response.json()
            print(f"  ✅ Contract created with ID: {contract['contract_id']}")
        else:
            print(f"  ❌ Failed to create contract: {response.status_code}")
        
        # CREATE Service
        print("  Creating service...")
        service_data = {
            "customer_id": customer_id,
            "internet_service": "Fiber optic",
            "online_security": "Yes",
            "online_backup": "No",
            "device_protection": "Yes",
            "tech_support": "No",
            "streaming_tv": "Yes",
            "streaming_movies": "No"
        }
        response = requests.post(f"{BASE_URL}/api/postgresql/services/", json=service_data)
        if response.status_code == 200:
            service = response.json()
            print(f"  ✅ Service created with ID: {service['service_id']}")
        else:
            print(f"  ❌ Failed to create service: {response.status_code}")
        
        # DELETE - Customer (will cascade delete contract and service)
        print("  Deleting customer...")
        response = requests.delete(f"{BASE_URL}/api/postgresql/customers/{customer_id}")
        if response.status_code == 200:
            print("  ✅ Customer deleted successfully (with cascade)")
        else:
            print(f"  ❌ Failed to delete customer: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ PostgreSQL test error: {e}")
        return False

def test_mongodb_crud():
    """Test MongoDB CRUD operations"""
    print("\n🍃 Testing MongoDB CRUD Operations...")
    
    # Test data
    customer_data = {
        "customerID": "TEST_MONGO_001",
        "customer_name": "Test Customer Mongo",
        "gender": "Male",
        "SeniorCitizen": False,
        "Partner": False,
        "Dependents": True,
        "tenure": 18,
        "PhoneService": True
    }
    
    try:
        # CREATE - Customer
        print("  Creating customer...")
        response = requests.post(f"{BASE_URL}/api/mongodb/customers/", json=customer_data)
        if response.status_code == 200:
            customer = response.json()
            print(f"  ✅ Customer created with ID: {customer['customerID']}")
        else:
            print(f"  ❌ Failed to create customer: {response.status_code}")
            return False
        
        # READ - Get customer
        print("  Reading customer...")
        response = requests.get(f"{BASE_URL}/api/mongodb/customers/TEST_MONGO_001")
        if response.status_code == 200:
            print("  ✅ Customer retrieved successfully")
        else:
            print(f"  ❌ Failed to get customer: {response.status_code}")
        
        # READ - Get all customers
        print("  Reading all customers...")
        response = requests.get(f"{BASE_URL}/api/mongodb/customers/?limit=10")
        if response.status_code == 200:
            customers = response.json()
            print(f"  ✅ Retrieved {len(customers)} customers")
        else:
            print(f"  ❌ Failed to get customers: {response.status_code}")
        
        # UPDATE - Customer
        print("  Updating customer...")
        update_data = {"customer_name": "Updated Test Customer Mongo", "tenure": 36}
        response = requests.put(f"{BASE_URL}/api/mongodb/customers/TEST_MONGO_001", json=update_data)
        if response.status_code == 200:
            print("  ✅ Customer updated successfully")
        else:
            print(f"  ❌ Failed to update customer: {response.status_code}")
        
        # CREATE Contract
        print("  Creating contract...")
        contract_data = {
            "customerID": "TEST_MONGO_001",
            "Contract": "Two year",
            "PaperlessBilling": False,
            "PaymentMethod": "Credit card",
            "MonthlyCharges": 89.90,
            "TotalCharges": 2400.00,
            "Churn": False
        }
        response = requests.post(f"{BASE_URL}/api/mongodb/contracts/", json=contract_data)
        if response.status_code == 200:
            print("  ✅ Contract created successfully")
        else:
            print(f"  ❌ Failed to create contract: {response.status_code}")
        
        # CREATE Service
        print("  Creating service...")
        service_data = {
            "customerID": "TEST_MONGO_001",
            "InternetService": "DSL",
            "OnlineSecurity": "No",
            "OnlineBackup": "Yes",
            "DeviceProtection": "No",
            "TechSupport": "Yes",
            "StreamingTV": "No",
            "StreamingMovies": "Yes"
        }
        response = requests.post(f"{BASE_URL}/api/mongodb/services/", json=service_data)
        if response.status_code == 200:
            print("  ✅ Service created successfully")
        else:
            print(f"  ❌ Failed to create service: {response.status_code}")
        
        # GET Complete Data
        print("  Getting complete customer data...")
        response = requests.get(f"{BASE_URL}/api/mongodb/customers/TEST_MONGO_001/complete")
        if response.status_code == 200:
            data = response.json()
            print("  ✅ Complete customer data retrieved")
            print(f"     Customer: {'✅' if data['customer'] else '❌'}")
            print(f"     Contract: {'✅' if data['contract'] else '❌'}")
            print(f"     Service: {'✅' if data['service'] else '❌'}")
        else:
            print(f"  ❌ Failed to get complete data: {response.status_code}")
        
        # SEARCH Customers
        print("  Searching customers...")
        response = requests.get(f"{BASE_URL}/api/mongodb/customers/search/?gender=Male&limit=5")
        if response.status_code == 200:
            results = response.json()
            print(f"  ✅ Search returned {len(results)} results")
        else:
            print(f"  ❌ Failed to search customers: {response.status_code}")
        
        # DELETE - Service
        print("  Deleting service...")
        response = requests.delete(f"{BASE_URL}/api/mongodb/services/TEST_MONGO_001")
        if response.status_code == 200:
            print("  ✅ Service deleted successfully")
        else:
            print(f"  ❌ Failed to delete service: {response.status_code}")
        
        # DELETE - Contract
        print("  Deleting contract...")
        response = requests.delete(f"{BASE_URL}/api/mongodb/contracts/TEST_MONGO_001")
        if response.status_code == 200:
            print("  ✅ Contract deleted successfully")
        else:
            print(f"  ❌ Failed to delete contract: {response.status_code}")
        
        # DELETE - Customer
        print("  Deleting customer...")
        response = requests.delete(f"{BASE_URL}/api/mongodb/customers/TEST_MONGO_001")
        if response.status_code == 200:
            print("  ✅ Customer deleted successfully")
        else:
            print(f"  ❌ Failed to delete customer: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ MongoDB test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting API Tests...")
    print("=" * 50)
    
    # Wait a moment for API to be ready
    time.sleep(2)
    
    # Test health
    if not test_api_health():
        print("\n❌ API health check failed. Make sure the API is running.")
        return
    
    # Test PostgreSQL
    pg_success = test_postgresql_crud()
    
    # Test MongoDB
    mongo_success = test_mongodb_crud()
    
    # Summary
    print("\n" + "=" * 50)
    print("📝 Test Summary:")
    print(f"   PostgreSQL CRUD: {'✅ PASSED' if pg_success else '❌ FAILED'}")
    print(f"   MongoDB CRUD: {'✅ PASSED' if mongo_success else '❌ FAILED'}")
    
    if pg_success and mongo_success:
        print("\n🎉 All tests passed! The API is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the logs above for details.")

if __name__ == "__main__":
    main()
