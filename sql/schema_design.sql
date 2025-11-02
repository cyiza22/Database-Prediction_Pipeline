-- Create Database
CREATE DATABASE telco_db;

\c telco_db;

-- ==============================
-- Table 1: Customers
-- ==============================
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    gender VARCHAR(10),
    senior_citizen BOOLEAN,
    partner BOOLEAN,
    dependents BOOLEAN,
    tenure INT,
    phone_service BOOLEAN
);

-- ==============================
-- Table 2: Contracts
-- ==============================
CREATE TABLE contracts (
    contract_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE,
    contract_type VARCHAR(50),
    paperless_billing BOOLEAN,
    payment_method VARCHAR(100),
    monthly_charges DECIMAL(10,2),
    total_charges DECIMAL(10,2),
    churn BOOLEAN
);

-- ==============================
-- Table 3: Services
-- ==============================
CREATE TABLE services (
    service_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE,
    internet_service VARCHAR(50),
    online_security VARCHAR(50),
    online_backup VARCHAR(50),
    device_protection VARCHAR(50),
    tech_support VARCHAR(50),
    streaming_tv VARCHAR(50),
    streaming_movies VARCHAR(50)
);

-- ==============================
-- Table 4: Contract Logs (for trigger)
-- ==============================
CREATE TABLE contract_logs (
    log_id SERIAL PRIMARY KEY,
    customer_id INT,
    old_total DECIMAL(10,2),
    new_total DECIMAL(10,2),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ==============================
-- STORED PROCEDURE
-- ==============================
-- Flags customers with high total charges as likely to churn
CREATE OR REPLACE FUNCTION flag_high_value_customers()
RETURNS VOID AS $$
BEGIN
    UPDATE contracts
    SET churn = TRUE
    WHERE total_charges > 5000 AND churn = FALSE;
END;
$$ LANGUAGE plpgsql;

-- ==============================
-- TRIGGER FUNCTION
-- ==============================
CREATE OR REPLACE FUNCTION log_contract_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO contract_logs (customer_id, old_total, new_total, updated_at)
    VALUES (OLD.customer_id, OLD.total_charges, NEW.total_charges, NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- TRIGGER

CREATE TRIGGER update_contract_log
AFTER UPDATE OF total_charges ON contracts
FOR EACH ROW
EXECUTE FUNCTION log_contract_update();
