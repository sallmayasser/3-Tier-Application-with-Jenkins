-- Create database
CREATE DATABASE shop;
-- Connect to it
\c shop;

-- Create table
CREATE TABLE customers (
    idx INT,
    customer_id INT,
    full_name TEXT,
    company TEXT,
    city TEXT,
    country TEXT,
    phone1 TEXT,
    phone2 TEXT,
    email TEXT,
    subscription_date DATE,
    website TEXT
);