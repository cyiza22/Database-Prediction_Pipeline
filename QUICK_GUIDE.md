# 🎯 Quick Reference Guide

## 📁 Folder Organization

### **src/** - Main Source Code
- **api/** - FastAPI web application
- **database/** - Database operations and connections
- **models/** - Data validation models (Pydantic schemas)

### **scripts/** - Utility Scripts
- **download_dataset.py** - Downloads Telco dataset from Kaggle
- **setup_databases.py** - Initializes PostgreSQL and MongoDB
- **mongo_setup.py** - MongoDB-specific setup

### **sql/** - SQL Scripts
- **schema_design.sql** - PostgreSQL database schema
- **insert_data.sql** - Sample data insertion queries

### **tests/** - Test Suite
- **test_api.py** - Comprehensive API endpoint testing

### **data/** - Data Storage
- Downloaded CSV files (gitignored)
- Data documentation

### **config/** - Configuration
- Environment variable templates

## 🚀 Quick Start Commands

```bash
# 1. Setup everything
python run_setup.py

# 2. Start API server
python app.py

# 3. Run tests
python tests/test_api.py

# 4. Access API docs
# Open: http://localhost:8000/docs
```

## 🏗️ Development Workflow

1. **Add new API endpoints** → Edit `src/api/main.py`
2. **Add data models** → Edit `src/models/models.py`
3. **Add database operations** → Edit `src/database/crud_*.py`
4. **Add tests** → Edit `tests/test_api.py`
5. **Database changes** → Edit `sql/*.sql`

## 📦 Project Benefits

✅ **Clean separation of concerns**
✅ **Easy to navigate and maintain**
✅ **Proper Python package structure**
✅ **Clear testing organization**
✅ **Configuration management**
✅ **Version control friendly**
