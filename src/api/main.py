from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional, Dict, Any
import uvicorn
from ..models.models import (
    Customer, CustomerCreate, CustomerUpdate,
    Contract, ContractCreate, ContractUpdate,
    Service, ServiceCreate, ServiceUpdate,
    CustomerMongo, ContractMongo, ServiceMongo,
    APIResponse
)
from ..database.crud_postgresql import CustomerCRUD, ContractCRUD, ServiceCRUD
from ..database.crud_mongodb import MongoCRUD
from ..database.database import test_pg_connection, test_mongo_connection

# Initialize FastAPI app
app = FastAPI(
    title="Telco Customer Churn API",
    description="API for managing Telco Customer data with PostgreSQL and MongoDB",
    version="1.0.0"
)

# Health check endpoints
@app.get("/", response_model=APIResponse)
async def root():
    """Root endpoint"""
    return APIResponse(message="Telco Customer Churn API is running!")

@app.get("/health", response_model=APIResponse)
async def health_check():
    """Health check endpoint"""
    pg_status = test_pg_connection()
    mongo_status = test_mongo_connection()
    
    return APIResponse(
        message="Health Check",
        data={
            "postgresql": "connected" if pg_status else "disconnected",
            "mongodb": "connected" if mongo_status else "disconnected",
            "overall": "healthy" if pg_status and mongo_status else "unhealthy"
        }
    )

# PostgreSQL Customer Endpoints
@app.post("/api/postgresql/customers/", response_model=Customer)
async def create_customer_pg(customer: CustomerCreate):
    """Create a new customer in PostgreSQL"""
    try:
        return CustomerCRUD.create_customer(customer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/postgresql/customers/{customer_id}", response_model=Customer)
async def get_customer_pg(customer_id: int):
    """Get a customer by ID from PostgreSQL"""
    customer = CustomerCRUD.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/api/postgresql/customers/", response_model=List[Customer])
async def get_customers_pg(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all customers from PostgreSQL with pagination"""
    return CustomerCRUD.get_customers(skip=skip, limit=limit)

@app.put("/api/postgresql/customers/{customer_id}", response_model=Customer)
async def update_customer_pg(customer_id: int, customer_update: CustomerUpdate):
    """Update a customer in PostgreSQL"""
    customer = CustomerCRUD.update_customer(customer_id, customer_update)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.delete("/api/postgresql/customers/{customer_id}", response_model=APIResponse)
async def delete_customer_pg(customer_id: int):
    """Delete a customer from PostgreSQL"""
    if not CustomerCRUD.delete_customer(customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return APIResponse(message="Customer deleted successfully")

# PostgreSQL Contract Endpoints
@app.post("/api/postgresql/contracts/", response_model=Contract)
async def create_contract_pg(contract: ContractCreate):
    """Create a new contract in PostgreSQL"""
    try:
        return ContractCRUD.create_contract(contract)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/postgresql/contracts/{contract_id}", response_model=Contract)
async def get_contract_pg(contract_id: int):
    """Get a contract by ID from PostgreSQL"""
    contract = ContractCRUD.get_contract(contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@app.get("/api/postgresql/contracts/", response_model=List[Contract])
async def get_contracts_pg(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all contracts from PostgreSQL with pagination"""
    return ContractCRUD.get_contracts(skip=skip, limit=limit)

@app.get("/api/postgresql/customers/{customer_id}/contracts/", response_model=List[Contract])
async def get_customer_contracts_pg(customer_id: int):
    """Get contracts by customer ID from PostgreSQL"""
    return ContractCRUD.get_contracts_by_customer(customer_id)

@app.put("/api/postgresql/contracts/{contract_id}", response_model=Contract)
async def update_contract_pg(contract_id: int, contract_update: ContractUpdate):
    """Update a contract in PostgreSQL"""
    contract = ContractCRUD.update_contract(contract_id, contract_update)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@app.delete("/api/postgresql/contracts/{contract_id}", response_model=APIResponse)
async def delete_contract_pg(contract_id: int):
    """Delete a contract from PostgreSQL"""
    if not ContractCRUD.delete_contract(contract_id):
        raise HTTPException(status_code=404, detail="Contract not found")
    return APIResponse(message="Contract deleted successfully")

# PostgreSQL Service Endpoints
@app.post("/api/postgresql/services/", response_model=Service)
async def create_service_pg(service: ServiceCreate):
    """Create a new service in PostgreSQL"""
    try:
        return ServiceCRUD.create_service(service)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/postgresql/services/{service_id}", response_model=Service)
async def get_service_pg(service_id: int):
    """Get a service by ID from PostgreSQL"""
    service = ServiceCRUD.get_service(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@app.get("/api/postgresql/services/", response_model=List[Service])
async def get_services_pg(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all services from PostgreSQL with pagination"""
    return ServiceCRUD.get_services(skip=skip, limit=limit)

@app.get("/api/postgresql/customers/{customer_id}/services/", response_model=List[Service])
async def get_customer_services_pg(customer_id: int):
    """Get services by customer ID from PostgreSQL"""
    return ServiceCRUD.get_services_by_customer(customer_id)

@app.put("/api/postgresql/services/{service_id}", response_model=Service)
async def update_service_pg(service_id: int, service_update: ServiceUpdate):
    """Update a service in PostgreSQL"""
    service = ServiceCRUD.update_service(service_id, service_update)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@app.delete("/api/postgresql/services/{service_id}", response_model=APIResponse)
async def delete_service_pg(service_id: int):
    """Delete a service from PostgreSQL"""
    if not ServiceCRUD.delete_service(service_id):
        raise HTTPException(status_code=404, detail="Service not found")
    return APIResponse(message="Service deleted successfully")

# MongoDB Customer Endpoints
@app.post("/api/mongodb/customers/", response_model=Dict[str, Any])
async def create_customer_mongo(customer: CustomerMongo):
    """Create a new customer in MongoDB"""
    try:
        return MongoCRUD.create_customer_mongo(customer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/mongodb/customers/{customer_id}", response_model=Dict[str, Any])
async def get_customer_mongo(customer_id: str):
    """Get a customer by ID from MongoDB"""
    customer = MongoCRUD.get_customer_mongo(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/api/mongodb/customers/", response_model=List[Dict[str, Any]])
async def get_customers_mongo(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all customers from MongoDB with pagination"""
    return MongoCRUD.get_customers_mongo(skip=skip, limit=limit)

@app.put("/api/mongodb/customers/{customer_id}", response_model=Dict[str, Any])
async def update_customer_mongo(customer_id: str, customer_update: Dict[str, Any]):
    """Update a customer in MongoDB"""
    customer = MongoCRUD.update_customer_mongo(customer_id, customer_update)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.delete("/api/mongodb/customers/{customer_id}", response_model=APIResponse)
async def delete_customer_mongo(customer_id: str):
    """Delete a customer from MongoDB"""
    if not MongoCRUD.delete_customer_mongo(customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return APIResponse(message="Customer deleted successfully")

# MongoDB Contract Endpoints
@app.post("/api/mongodb/contracts/", response_model=Dict[str, Any])
async def create_contract_mongo(contract: ContractMongo):
    """Create a new contract in MongoDB"""
    try:
        return MongoCRUD.create_contract_mongo(contract)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/mongodb/contracts/{customer_id}", response_model=Dict[str, Any])
async def get_contract_mongo(customer_id: str):
    """Get a contract by customer ID from MongoDB"""
    contract = MongoCRUD.get_contract_mongo(customer_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@app.get("/api/mongodb/contracts/", response_model=List[Dict[str, Any]])
async def get_contracts_mongo(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all contracts from MongoDB with pagination"""
    return MongoCRUD.get_contracts_mongo(skip=skip, limit=limit)

@app.put("/api/mongodb/contracts/{customer_id}", response_model=Dict[str, Any])
async def update_contract_mongo(customer_id: str, contract_update: Dict[str, Any]):
    """Update a contract in MongoDB"""
    contract = MongoCRUD.update_contract_mongo(customer_id, contract_update)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@app.delete("/api/mongodb/contracts/{customer_id}", response_model=APIResponse)
async def delete_contract_mongo(customer_id: str):
    """Delete a contract from MongoDB"""
    if not MongoCRUD.delete_contract_mongo(customer_id):
        raise HTTPException(status_code=404, detail="Contract not found")
    return APIResponse(message="Contract deleted successfully")

# MongoDB Service Endpoints
@app.post("/api/mongodb/services/", response_model=Dict[str, Any])
async def create_service_mongo(service: ServiceMongo):
    """Create a new service in MongoDB"""
    try:
        return MongoCRUD.create_service_mongo(service)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/mongodb/services/{customer_id}", response_model=Dict[str, Any])
async def get_service_mongo(customer_id: str):
    """Get a service by customer ID from MongoDB"""
    service = MongoCRUD.get_service_mongo(customer_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@app.get("/api/mongodb/services/", response_model=List[Dict[str, Any]])
async def get_services_mongo(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all services from MongoDB with pagination"""
    return MongoCRUD.get_services_mongo(skip=skip, limit=limit)

@app.put("/api/mongodb/services/{customer_id}", response_model=Dict[str, Any])
async def update_service_mongo(customer_id: str, service_update: Dict[str, Any]):
    """Update a service in MongoDB"""
    service = MongoCRUD.update_service_mongo(customer_id, service_update)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@app.delete("/api/mongodb/services/{customer_id}", response_model=APIResponse)
async def delete_service_mongo(customer_id: str):
    """Delete a service from MongoDB"""
    if not MongoCRUD.delete_service_mongo(customer_id):
        raise HTTPException(status_code=404, detail="Service not found")
    return APIResponse(message="Service deleted successfully")

# MongoDB Utility Endpoints
@app.get("/api/mongodb/customers/{customer_id}/complete", response_model=Dict[str, Any])
async def get_customer_complete_data_mongo(customer_id: str):
    """Get complete customer data from MongoDB (customer + contract + service)"""
    data = MongoCRUD.get_customer_complete_data(customer_id)
    if not data["customer"]:
        raise HTTPException(status_code=404, detail="Customer not found")
    return data

@app.get("/api/mongodb/customers/search/", response_model=List[Dict[str, Any]])
async def search_customers_mongo(
    gender: Optional[str] = None,
    senior_citizen: Optional[bool] = None,
    partner: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Search customers by criteria in MongoDB"""
    criteria = {}
    if gender:
        criteria["gender"] = gender
    if senior_citizen is not None:
        criteria["SeniorCitizen"] = senior_citizen
    if partner is not None:
        criteria["Partner"] = partner
    
    return MongoCRUD.search_customers_by_criteria(criteria, skip=skip, limit=limit)

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
