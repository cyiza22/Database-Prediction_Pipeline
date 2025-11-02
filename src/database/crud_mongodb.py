from typing import List, Optional, Dict, Any
from .database import get_mongo_collection
from ..models.models import CustomerMongo, ContractMongo, ServiceMongo
from bson import ObjectId
import pymongo

# MongoDB CRUD Operations
class MongoCRUD:
    
    # Customer Operations
    @staticmethod
    def create_customer_mongo(customer: CustomerMongo) -> Dict[str, Any]:
        """Create a new customer in MongoDB"""
        with get_mongo_collection("customers") as collection:
            customer_dict = customer.dict()
            result = collection.insert_one(customer_dict)
            customer_dict["_id"] = str(result.inserted_id)
            return customer_dict
    
    @staticmethod
    def get_customer_mongo(customer_id: str) -> Optional[Dict[str, Any]]:
        """Get a customer by customerID"""
        with get_mongo_collection("customers") as collection:
            result = collection.find_one({"customerID": customer_id})
            if result:
                result["_id"] = str(result["_id"])
            return result
    
    @staticmethod
    def get_customers_mongo(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all customers with pagination"""
        with get_mongo_collection("customers") as collection:
            results = collection.find().skip(skip).limit(limit)
            customers = []
            for result in results:
                result["_id"] = str(result["_id"])
                customers.append(result)
            return customers
    
    @staticmethod
    def update_customer_mongo(customer_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a customer in MongoDB"""
        with get_mongo_collection("customers") as collection:
            # Remove None values
            update_data = {k: v for k, v in update_data.items() if v is not None}
            if not update_data:
                return MongoCRUD.get_customer_mongo(customer_id)
            
            result = collection.find_one_and_update(
                {"customerID": customer_id},
                {"$set": update_data},
                return_document=pymongo.ReturnDocument.AFTER
            )
            if result:
                result["_id"] = str(result["_id"])
            return result
    
    @staticmethod
    def delete_customer_mongo(customer_id: str) -> bool:
        """Delete a customer from MongoDB"""
        with get_mongo_collection("customers") as collection:
            result = collection.delete_one({"customerID": customer_id})
            return result.deleted_count > 0
    
    # Contract Operations
    @staticmethod
    def create_contract_mongo(contract: ContractMongo) -> Dict[str, Any]:
        """Create a new contract in MongoDB"""
        with get_mongo_collection("contracts") as collection:
            contract_dict = contract.dict()
            result = collection.insert_one(contract_dict)
            contract_dict["_id"] = str(result.inserted_id)
            return contract_dict
    
    @staticmethod
    def get_contract_mongo(customer_id: str) -> Optional[Dict[str, Any]]:
        """Get a contract by customerID"""
        with get_mongo_collection("contracts") as collection:
            result = collection.find_one({"customerID": customer_id})
            if result:
                result["_id"] = str(result["_id"])
            return result
    
    @staticmethod
    def get_contracts_mongo(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all contracts with pagination"""
        with get_mongo_collection("contracts") as collection:
            results = collection.find().skip(skip).limit(limit)
            contracts = []
            for result in results:
                result["_id"] = str(result["_id"])
                contracts.append(result)
            return contracts
    
    @staticmethod
    def update_contract_mongo(customer_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a contract in MongoDB"""
        with get_mongo_collection("contracts") as collection:
            # Remove None values
            update_data = {k: v for k, v in update_data.items() if v is not None}
            if not update_data:
                return MongoCRUD.get_contract_mongo(customer_id)
            
            result = collection.find_one_and_update(
                {"customerID": customer_id},
                {"$set": update_data},
                return_document=pymongo.ReturnDocument.AFTER
            )
            if result:
                result["_id"] = str(result["_id"])
            return result
    
    @staticmethod
    def delete_contract_mongo(customer_id: str) -> bool:
        """Delete a contract from MongoDB"""
        with get_mongo_collection("contracts") as collection:
            result = collection.delete_one({"customerID": customer_id})
            return result.deleted_count > 0
    
    # Service Operations
    @staticmethod
    def create_service_mongo(service: ServiceMongo) -> Dict[str, Any]:
        """Create a new service in MongoDB"""
        with get_mongo_collection("services") as collection:
            service_dict = service.dict()
            result = collection.insert_one(service_dict)
            service_dict["_id"] = str(result.inserted_id)
            return service_dict
    
    @staticmethod
    def get_service_mongo(customer_id: str) -> Optional[Dict[str, Any]]:
        """Get a service by customerID"""
        with get_mongo_collection("services") as collection:
            result = collection.find_one({"customerID": customer_id})
            if result:
                result["_id"] = str(result["_id"])
            return result
    
    @staticmethod
    def get_services_mongo(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all services with pagination"""
        with get_mongo_collection("services") as collection:
            results = collection.find().skip(skip).limit(limit)
            services = []
            for result in results:
                result["_id"] = str(result["_id"])
                services.append(result)
            return services
    
    @staticmethod
    def update_service_mongo(customer_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a service in MongoDB"""
        with get_mongo_collection("services") as collection:
            # Remove None values
            update_data = {k: v for k, v in update_data.items() if v is not None}
            if not update_data:
                return MongoCRUD.get_service_mongo(customer_id)
            
            result = collection.find_one_and_update(
                {"customerID": customer_id},
                {"$set": update_data},
                return_document=pymongo.ReturnDocument.AFTER
            )
            if result:
                result["_id"] = str(result["_id"])
            return result
    
    @staticmethod
    def delete_service_mongo(customer_id: str) -> bool:
        """Delete a service from MongoDB"""
        with get_mongo_collection("services") as collection:
            result = collection.delete_one({"customerID": customer_id})
            return result.deleted_count > 0
    
    # Utility Operations
    @staticmethod
    def get_customer_complete_data(customer_id: str) -> Dict[str, Any]:
        """Get complete customer data (customer + contract + service)"""
        customer = MongoCRUD.get_customer_mongo(customer_id)
        contract = MongoCRUD.get_contract_mongo(customer_id)
        service = MongoCRUD.get_service_mongo(customer_id)
        
        return {
            "customer": customer,
            "contract": contract,
            "service": service
        }
    
    @staticmethod
    def search_customers_by_criteria(criteria: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Search customers by various criteria"""
        with get_mongo_collection("customers") as collection:
            results = collection.find(criteria).skip(skip).limit(limit)
            customers = []
            for result in results:
                result["_id"] = str(result["_id"])
                customers.append(result)
            return customers
