-- schema.sql

-- Step 1: Create database
CREATE DATABASE u_sell_it;

-- Step 2: Connect to database
\c u_sell_it

-- Step 3: Create users table
CREATE TABLE public.users (
    user_id        SERIAL PRIMARY KEY,
    first_name     VARCHAR(100),
    last_name      VARCHAR(100),
    username       VARCHAR(255) NOT NULL UNIQUE,
    email          VARCHAR(255) NOT NULL UNIQUE,
    password       VARCHAR(255) NOT NULL,
    phone          VARCHAR(20),
    street_address TEXT,
    city           VARCHAR(100),
    zip_code       VARCHAR(20),
    state          VARCHAR(50)
);
