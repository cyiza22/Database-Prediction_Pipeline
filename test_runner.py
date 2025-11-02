#!/usr/bin/env python3
"""
Test runner for Database Prediction Pipeline - Task 2 Validation
"""

import sys
import os
import subprocess
import time

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_imports():
    """Test if all modules can be imported correctly"""
    print("🔍 Testing module imports...")
    
    try:
        # Test API imports
        from src.api.main import app
        print("✅ API module imports successfully")
        
        # Test database imports
        from src.database.database import test_pg_connection, test_mongo_connection
        from src.database.crud_postgresql import CustomerCRUD, ContractCRUD, ServiceCRUD
        from src.database.crud_mongodb import MongoCRUD
        print("✅ Database modules import successfully")
        
        # Test models
        from src.models.models import Customer, CustomerCreate, Contract, Service
        print("✅ Model modules import successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_connections():
    """Test database connections"""
    print("\n🔗 Testing database connections...")
    
    try:
        from src.database.database import test_pg_connection, test_mongo_connection
        
        # Test PostgreSQL
        print("Testing PostgreSQL connection...")
        pg_result = test_pg_connection()
        if pg_result:
            print("✅ PostgreSQL connection successful")
        else:
            print("❌ PostgreSQL connection failed")
            
        # Test MongoDB
        print("Testing MongoDB connection...")
        mongo_result = test_mongo_connection()
        if mongo_result:
            print("✅ MongoDB connection successful")
        else:
            print("❌ MongoDB connection failed")
            
        return pg_result and mongo_result
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def run_api_tests():
    """Run the API endpoint tests"""
    print("\n🧪 Running API endpoint tests...")
    
    try:
        # Run the test file
        result = subprocess.run([
            sys.executable, "tests/test_api.py"
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ All API tests passed!")
            print(result.stdout)
            return True
        else:
            print("❌ Some API tests failed:")
            print(result.stderr)
            print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 Starting Task 2 Validation Tests...")
    print("=" * 50)
    
    # Test 1: Module imports
    if not test_imports():
        print("\n❌ Import tests failed. Please check your code structure.")
        return False
    
    # Test 2: Database connections
    if not test_database_connections():
        print("\n❌ Database connection tests failed. Please check your environment variables.")
        return False
    
    # Test 3: API endpoint tests
    if not run_api_tests():
        print("\n❌ API tests failed. Please check your implementation.")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL TASK 2 TESTS PASSED SUCCESSFULLY!")
    print("✅ Your FastAPI CRUD operations are working correctly")
    print("✅ Database connections are established")
    print("✅ All endpoints are functioning as expected")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
