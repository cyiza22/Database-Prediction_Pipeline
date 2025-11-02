from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Customer Models
class CustomerBase(BaseModel):
    customer_name: str
    gender: str
    senior_citizen: bool
    partner: bool
    dependents: bool
    tenure: int
    phone_service: bool

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    gender: Optional[str] = None
    senior_citizen: Optional[bool] = None
    partner: Optional[bool] = None
    dependents: Optional[bool] = None
    tenure: Optional[int] = None
    phone_service: Optional[bool] = None

class Customer(CustomerBase):
    customer_id: int
    
    class Config:
        from_attributes = True

# Contract Models
class ContractBase(BaseModel):
    contract_type: str
    paperless_billing: bool
    payment_method: str
    monthly_charges: float
    total_charges: float
    churn: bool

class ContractCreate(ContractBase):
    customer_id: int

class ContractUpdate(BaseModel):
    contract_type: Optional[str] = None
    paperless_billing: Optional[bool] = None
    payment_method: Optional[str] = None
    monthly_charges: Optional[float] = None
    total_charges: Optional[float] = None
    churn: Optional[bool] = None

class Contract(ContractBase):
    contract_id: int
    customer_id: int
    
    class Config:
        from_attributes = True

# Service Models
class ServiceBase(BaseModel):
    internet_service: str
    online_security: str
    online_backup: str
    device_protection: str
    tech_support: str
    streaming_tv: str
    streaming_movies: str

class ServiceCreate(ServiceBase):
    customer_id: int

class ServiceUpdate(BaseModel):
    internet_service: Optional[str] = None
    online_security: Optional[str] = None
    online_backup: Optional[str] = None
    device_protection: Optional[str] = None
    tech_support: Optional[str] = None
    streaming_tv: Optional[str] = None
    streaming_movies: Optional[str] = None

class Service(ServiceBase):
    service_id: int
    customer_id: int
    
    class Config:
        from_attributes = True

# MongoDB Models (using dict structure)
class CustomerMongo(BaseModel):
    customerID: str
    customer_name: str
    gender: str
    SeniorCitizen: bool
    Partner: bool
    Dependents: bool
    tenure: int
    PhoneService: bool

class ContractMongo(BaseModel):
    customerID: str
    Contract: str
    PaperlessBilling: bool
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float
    Churn: bool

class ServiceMongo(BaseModel):
    customerID: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str

# Response Models
class APIResponse(BaseModel):
    message: str
    data: Optional[dict] = None
    count: Optional[int] = None
