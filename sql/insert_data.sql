INSERT INTO customers (customer_name, gender, senior_citizen, partner, dependents, tenure, phone_service)
VALUES
('Alice Johnson', 'Female', FALSE, TRUE, FALSE, 12, TRUE),
('Bob Smith', 'Male', TRUE, FALSE, TRUE, 24, TRUE),
('Clara Niyonsaba', 'Female', FALSE, FALSE, FALSE, 6, TRUE);

INSERT INTO contracts (customer_id, contract_type, paperless_billing, payment_method, monthly_charges, total_charges, churn)
VALUES
(1, 'Month-to-month', TRUE, 'Electronic check', 70.35, 1000.00, FALSE),
(2, 'One year', FALSE, 'Credit card', 89.10, 5400.00, FALSE),
(3, 'Two year', TRUE, 'Bank transfer', 65.20, 800.00, FALSE);

INSERT INTO services (customer_id, internet_service, online_security, online_backup, device_protection, tech_support, streaming_tv, streaming_movies)
VALUES
(1, 'Fiber optic', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'No'),
(2, 'DSL', 'No', 'No', 'Yes', 'Yes', 'No', 'Yes'),
(3, 'Fiber optic', 'Yes', 'No', 'No', 'No', 'Yes', 'Yes');
