# Database Prediction Pipeline - Telco Customer Churn

A comprehensive database management and API system built with FastAPI, PostgreSQL, and MongoDB for the Telco Customer Churn dataset.

##  Project Overview

This project implements a complete database pipeline with:
- **Task 1**: Database design and implementation (SQL and NoSQL)
- **Task 2**: RESTful API with CRUD operations using FastAPI

## 📋 Features

### Task 1 - Database Implementation 
- **PostgreSQL Database**: Relational database with 4 tables
  - `customers`: Customer demographic information
  - `contracts`: Contract and billing details
  - `services`: Service subscriptions
  - `contract_logs`: Audit logs for contract changes
- **MongoDB Database**: NoSQL collections mirroring SQL structure
- **Stored Procedure**: `flag_high_value_customers()` for churn prediction
- **Trigger**: Automatic logging of contract changes
- **ERD Documentation**: Complete entity relationship diagram specification

### Task 2 - FastAPI CRUD Operations 
- **PostgreSQL Endpoints**: Full CRUD for all tables
- **MongoDB Endpoints**: Full CRUD for all collections
- **Health Monitoring**: Database connection status
- **Interactive Documentation**: Swagger UI at `/docs`
- **Data Validation**: Pydantic models for request/response validation

##  Project Structure

```
Database-Prediction_Pipeline/
├── 📁 src/                        # Source code
│   ├── 📁 api/                    # FastAPI application
│   │   ├── __init__.py
│   │   └── main.py               # Main API application
│   ├── 📁 database/              # Database operations
│   │   ├── __init__.py
│   │   ├── database.py           # Database connections
│   │   ├── crud_postgresql.py    # PostgreSQL CRUD operations
│   │   └── crud_mongodb.py       # MongoDB CRUD operations
│   ├── 📁 models/                # Data models
│   │   ├── __init__.py
│   │   └── models.py             # Pydantic models
│   └── __init__.py
├── 📁 scripts/                    # Setup and utility scripts
│   ├── download_dataset.py       # Kaggle dataset downloader
│   ├── mongo_setup.py            # MongoDB initialization
│   └── setup_databases.py        # Database setup automation
├── 📁 sql/                       # SQL scripts
│   ├── schema_design.sql         # PostgreSQL schema
│   └── insert_data.sql           # Sample data insertion
├── 📁 tests/                     # Test files
│   ├── __init__.py
│   └── test_api.py              # API endpoint tests
├── 📁 data/                      # Data files
│   ├── README.md                # Data directory documentation
│   └── *.csv                    # Downloaded datasets (gitignored)
├── 📁 config/                    # Configuration files
│   └── .env.template            # Environment variables template
├── 📄 app.py                     # Main application entry point
├── 📄 run_setup.py              # Complete setup automation
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env                      # Environment variables (create manually)
├── 📄 .gitignore               # Git ignore rules
└── 📄 README.md                # Project documentation
```

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- MongoDB 4.4+
- Kaggle API credentials (optional, for dataset download)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd Database-Prediction_Pipeline
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.template .env

# Edit .env with your database credentials
# Configure PostgreSQL and MongoDB connection settings
```

### 3. **Automated Setup**
   ```bash
   python run_setup.py
   ```
   
   This will:
   - Install Python dependencies
   - Download the Telco dataset from Kaggle
   - Set up PostgreSQL and MongoDB databases
   
4. **Start the API Server**
   ```bash
   python app.py
   ```
   
   Or manually:
   ```bash
   uvicorn src.api.main:app --reload
   ```

##  API Documentation

Once the server is running:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### PostgreSQL Endpoints

#### Customers
- `POST /api/postgresql/customers/` - Create customer
- `GET /api/postgresql/customers/{id}` - Get customer by ID
- `GET /api/postgresql/customers/` - List customers (paginated)
- `PUT /api/postgresql/customers/{id}` - Update customer
- `DELETE /api/postgresql/customers/{id}` - Delete customer

#### Contracts
- `POST /api/postgresql/contracts/` - Create contract
- `GET /api/postgresql/contracts/{id}` - Get contract by ID
- `GET /api/postgresql/contracts/` - List contracts (paginated)
- `GET /api/postgresql/customers/{id}/contracts/` - Get customer contracts
- `PUT /api/postgresql/contracts/{id}` - Update contract
- `DELETE /api/postgresql/contracts/{id}` - Delete contract

#### Services
- `POST /api/postgresql/services/` - Create service
- `GET /api/postgresql/services/{id}` - Get service by ID
- `GET /api/postgresql/services/` - List services (paginated)
- `GET /api/postgresql/customers/{id}/services/` - Get customer services
- `PUT /api/postgresql/services/{id}` - Update service
- `DELETE /api/postgresql/services/{id}` - Delete service

### MongoDB Endpoints

#### Customers
- `POST /api/mongodb/customers/` - Create customer
- `GET /api/mongodb/customers/{customerID}` - Get customer by customerID
- `GET /api/mongodb/customers/` - List customers (paginated)
- `PUT /api/mongodb/customers/{customerID}` - Update customer
- `DELETE /api/mongodb/customers/{customerID}` - Delete customer

#### Contracts
- `POST /api/mongodb/contracts/` - Create contract
- `GET /api/mongodb/contracts/{customerID}` - Get contract by customerID
- `GET /api/mongodb/contracts/` - List contracts (paginated)
- `PUT /api/mongodb/contracts/{customerID}` - Update contract
- `DELETE /api/mongodb/contracts/{customerID}` - Delete contract

#### Services
- `POST /api/mongodb/services/` - Create service
- `GET /api/mongodb/services/{customerID}` - Get service by customerID
- `GET /api/mongodb/services/` - List services (paginated)
- `PUT /api/mongodb/services/{customerID}` - Update service
- `DELETE /api/mongodb/services/{customerID}` - Delete service

#### Utility Endpoints
- `GET /api/mongodb/customers/{customerID}/complete` - Get complete customer data
- `GET /api/mongodb/customers/search/` - Search customers by criteria

##  Testing

### API Testing
```bash
# Start the API server
python app.py

# Run tests in another terminal
python tests/test_api.py
```

### Manual Testing
Use the interactive documentation at http://localhost:8000/docs to test individual endpoints.

##  Database Schema

### PostgreSQL Tables

#### customers
- `customer_id` (PK, SERIAL)
- `customer_name` (VARCHAR)
- `gender` (VARCHAR)
- `senior_citizen` (BOOLEAN)
- `partner` (BOOLEAN)
- `dependents` (BOOLEAN)
- `tenure` (INT)
- `phone_service` (BOOLEAN)

#### contracts
- `contract_id` (PK, SERIAL)
- `customer_id` (FK → customers.customer_id)
- `contract_type` (VARCHAR)
- `paperless_billing` (BOOLEAN)
- `payment_method` (VARCHAR)
- `monthly_charges` (DECIMAL)
- `total_charges` (DECIMAL)
- `churn` (BOOLEAN)

#### services
- `service_id` (PK, SERIAL)
- `customer_id` (FK → customers.customer_id)
- `internet_service` (VARCHAR)
- `online_security` (VARCHAR)
- `online_backup` (VARCHAR)
- `device_protection` (VARCHAR)
- `tech_support` (VARCHAR)
- `streaming_tv` (VARCHAR)
- `streaming_movies` (VARCHAR)

#### contract_logs
- `log_id` (PK, SERIAL)
- `customer_id` (INT)
- `old_total` (DECIMAL)
- `new_total` (DECIMAL)
- `updated_at` (TIMESTAMP)

### MongoDB Collections
- `customers` - Customer documents with demographic data
- `contracts` - Contract documents with billing information
- `services` - Service documents with subscription details

##  Dataset

The project uses the **Telco Customer Churn Dataset** from Kaggle:
- **Source**: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- **Size**: ~7,000 customer records
- **Features**: 21 columns including demographics, services, and churn status

##  Database Features

### Stored Procedure
```sql
-- Flags customers with high total charges as likely to churn
CREATE OR REPLACE FUNCTION flag_high_value_customers()
RETURNS VOID AS $$
BEGIN
    UPDATE contracts
    SET churn = TRUE
    WHERE total_charges > 5000 AND churn = FALSE;
END;
$$ LANGUAGE plpgsql;
```

### Trigger
```sql
-- Automatically logs changes to total_charges
CREATE TRIGGER update_contract_log
AFTER UPDATE OF total_charges ON contracts
FOR EACH ROW
EXECUTE FUNCTION log_contract_update();
```

##  Environment Variables

Create a `.env` file with the following configuration:

```env
# PostgreSQL Configuration
PG_HOST=localhost
PG_PORT=5432
PG_DB=telco_db
PG_USER=your_postgres_username
PG_PASSWORD=your_postgres_password

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=telco_mongo_db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

##  Task Completion Status

### Task 1 - Database Implementation
- [x] PostgreSQL database with 4+ tables
- [x] Primary and foreign key relationships
- [x] MongoDB collections implementation
- [x] Stored procedure for automation
- [x] Trigger for data logging
- [x] ERD diagram specification
- [x] Kaggle dataset integration

###  Task 2 - FastAPI CRUD Operations
- [x] POST endpoints (Create operations)
- [x] GET endpoints (Read operations)
- [x] PUT endpoints (Update operations)
- [x] DELETE endpoints (Delete operations)
- [x] PostgreSQL integration
- [x] MongoDB integration
- [x] Data validation with Pydantic
- [x] Error handling and status codes
- [x] API documentation

##  Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure PostgreSQL and MongoDB are running
   - Check database credentials in `.env`
   - Verify database names exist

2. **Import Errors**
   - Install requirements: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Dataset Not Found**
   - Run `python scripts/download_dataset.py`
   - Ensure Kaggle API credentials are configured

4. **API Server Won't Start**
   - Check if port 8000 is available
   - Verify all dependencies are installed

## Team Contributions

Document your team member contributions in the final report:
- Database design and implementation
- API endpoint development
- Testing and validation
- Documentation and ERD creation

##  License

This project is created for educational purposes as part of a database and API development assignment.


