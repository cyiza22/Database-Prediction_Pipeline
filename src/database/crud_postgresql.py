from typing import List, Optional
from .database import get_pg_cursor
from ..models.models import Customer, CustomerCreate, CustomerUpdate, Contract, ContractCreate, ContractUpdate, Service, ServiceCreate, ServiceUpdate

# Customer CRUD Operations
class CustomerCRUD:
    
    @staticmethod
    def create_customer(customer: CustomerCreate) -> Customer:
        """Create a new customer"""
        with get_pg_cursor() as cursor:
            cursor.execute("""
                INSERT INTO customers (customer_name, gender, senior_citizen, partner, dependents, tenure, phone_service)
                VALUES (%(customer_name)s, %(gender)s, %(senior_citizen)s, %(partner)s, %(dependents)s, %(tenure)s, %(phone_service)s)
                RETURNING customer_id, customer_name, gender, senior_citizen, partner, dependents, tenure, phone_service
            """, customer.dict())
            result = cursor.fetchone()
            return Customer(**result)
    
    @staticmethod
    def get_customer(customer_id: int) -> Optional[Customer]:
        """Get a customer by ID"""
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            result = cursor.fetchone()
            return Customer(**result) if result else None
    
    @staticmethod
    def get_customers(skip: int = 0, limit: int = 100) -> List[Customer]:
        """Get all customers with pagination"""
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM customers ORDER BY customer_id OFFSET %s LIMIT %s", (skip, limit))
            results = cursor.fetchall()
            return [Customer(**row) for row in results]
    
    @staticmethod
    def update_customer(customer_id: int, customer_update: CustomerUpdate) -> Optional[Customer]:
        """Update a customer"""
        update_data = {k: v for k, v in customer_update.dict().items() if v is not None}
        if not update_data:
            return CustomerCRUD.get_customer(customer_id)
        
        set_clause = ", ".join([f"{k} = %({k})s" for k in update_data.keys()])
        update_data['customer_id'] = customer_id
        
        with get_pg_cursor() as cursor:
            cursor.execute(f"""
                UPDATE customers SET {set_clause}
                WHERE customer_id = %(customer_id)s
                RETURNING customer_id, customer_name, gender, senior_citizen, partner, dependents, tenure, phone_service
            """, update_data)
            result = cursor.fetchone()
            return Customer(**result) if result else None
    
    @staticmethod
    def delete_customer(customer_id: int) -> bool:
        """Delete a customer"""
        with get_pg_cursor() as cursor:
            cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
            return cursor.rowcount > 0

# Contract CRUD Operations
class ContractCRUD:
    
    @staticmethod
    def create_contract(contract: ContractCreate) -> Contract:
        """Create a new contract"""
        with get_pg_cursor() as cursor:
            cursor.execute("""
                INSERT INTO contracts (customer_id, contract_type, paperless_billing, payment_method, monthly_charges, total_charges, churn)
                VALUES (%(customer_id)s, %(contract_type)s, %(paperless_billing)s, %(payment_method)s, %(monthly_charges)s, %(total_charges)s, %(churn)s)
                RETURNING contract_id, customer_id, contract_type, paperless_billing, payment_method, monthly_charges, total_charges, churn
            """, contract.dict())
            result = cursor.fetchone()
            return Contract(**result)
    
    @staticmethod
    def get_contract(contract_id: int) -> Optional[Contract]:
        """Get a contract by ID"""
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM contracts WHERE contract_id = %s", (contract_id,))
            result = cursor.fetchone()
            return Contract(**result) if result else None
    
    @staticmethod
    def get_contracts(skip: int = 0, limit: int = 100) -> List[Contract]:
        """Get all contracts with pagination"""
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM contracts ORDER BY contract_id OFFSET %s LIMIT %s", (skip, limit))
            results = cursor.fetchall()
            return [Contract(**row) for row in results]
    
    @staticmethod
    def get_contracts_by_customer(customer_id: int) -> List[Contract]:
        """Get contracts by customer ID"""
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM contracts WHERE customer_id = %s", (customer_id,))
            results = cursor.fetchall()
            return [Contract(**row) for row in results]
    
    @staticmethod
    def update_contract(contract_id: int, contract_update: ContractUpdate) -> Optional[Contract]:
        """Update a contract"""
        update_data = {k: v for k, v in contract_update.dict().items() if v is not None}
        if not update_data:
            return ContractCRUD.get_contract(contract_id)
        
        set_clause = ", ".join([f"{k} = %({k})s" for k in update_data.keys()])
        update_data['contract_id'] = contract_id
        
        with get_pg_cursor() as cursor:
            cursor.execute(f"""
                UPDATE contracts SET {set_clause}
                WHERE contract_id = %(contract_id)s
                RETURNING contract_id, customer_id, contract_type, paperless_billing, payment_method, monthly_charges, total_charges, churn
            """, update_data)
            result = cursor.fetchone()
            return Contract(**result) if result else None
    
    @staticmethod
    def delete_contract(contract_id: int) -> bool:
        """Delete a contract"""
        with get_pg_cursor() as cursor:
            cursor.execute("DELETE FROM contracts WHERE contract_id = %s", (contract_id,))
            return cursor.rowcount > 0

# Service CRUD Operations
class ServiceCRUD:
    
    @staticmethod
    def create_service(service: ServiceCreate) -> Service:
        """Create a new service"""
        with get_pg_cursor() as cursor:
            cursor.execute("""
                INSERT INTO services (customer_id, internet_service, online_security, online_backup, device_protection, tech_support, streaming_tv, streaming_movies)
                VALUES (%(customer_id)s, %(internet_service)s, %(online_security)s, %(online_backup)s, %(device_protection)s, %(tech_support)s, %(streaming_tv)s, %(streaming_movies)s)
                RETURNING service_id, customer_id, internet_service, online_security, online_backup, device_protection, tech_support, streaming_tv, streaming_movies
            """, service.dict())
            result = cursor.fetchone()
            return Service(**result)
    
    @staticmethod
    def get_service(service_id: int) -> Optional[Service]:
        """Get a service by ID"""
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM services WHERE service_id = %s", (service_id,))
            result = cursor.fetchone()
            return Service(**result) if result else None
    
    @staticmethod
    def get_services(skip: int = 0, limit: int = 100) -> List[Service]:
        """Get all services with pagination"""
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM services ORDER BY service_id OFFSET %s LIMIT %s", (skip, limit))
            results = cursor.fetchall()
            return [Service(**row) for row in results]
    
    @staticmethod
    def get_services_by_customer(customer_id: int) -> List[Service]:
        """Get services by customer ID"""
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM services WHERE customer_id = %s", (customer_id,))
            results = cursor.fetchall()
            return [Service(**row) for row in results]
    
    @staticmethod
    def update_service(service_id: int, service_update: ServiceUpdate) -> Optional[Service]:
        """Update a service"""
        update_data = {k: v for k, v in service_update.dict().items() if v is not None}
        if not update_data:
            return ServiceCRUD.get_service(service_id)
        
        set_clause = ", ".join([f"{k} = %({k})s" for k in update_data.keys()])
        update_data['service_id'] = service_id
        
        with get_pg_cursor() as cursor:
            cursor.execute(f"""
                UPDATE services SET {set_clause}
                WHERE service_id = %(service_id)s
                RETURNING service_id, customer_id, internet_service, online_security, online_backup, device_protection, tech_support, streaming_tv, streaming_movies
            """, update_data)
            result = cursor.fetchone()
            return Service(**result) if result else None
    
    @staticmethod
    def delete_service(service_id: int) -> bool:
        """Delete a service"""
        with get_pg_cursor() as cursor:
            cursor.execute("DELETE FROM services WHERE service_id = %s", (service_id,))
            return cursor.rowcount > 0
