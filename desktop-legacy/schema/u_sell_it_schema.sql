-- =========================================================
-- u_sell_it Database Schema
-- PostgreSQL schema for marketplace simulation
-- =========================================================

-- Drop existing tables if you want a clean reset
DROP TABLE IF EXISTS favorites CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS watchlist CASCADE;
DROP TABLE IF EXISTS items CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- =========================================================
-- Users
-- =========================================================
CREATE TABLE users (
    user_id         SERIAL PRIMARY KEY,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    username        VARCHAR(50) UNIQUE NOT NULL,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    phone           VARCHAR(20),
    street_address  TEXT,
    city            VARCHAR(100),
    state           VARCHAR(50),
    zip_code        VARCHAR(20),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- Items (listings for sale)
-- =========================================================
CREATE TABLE items (
    item_id         SERIAL PRIMARY KEY,
    seller_id       INT REFERENCES users(user_id) ON DELETE CASCADE,
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    category        VARCHAR(100),
    price           NUMERIC(10,2) NOT NULL,
    status          VARCHAR(20) DEFAULT 'available', -- available, sold, removed
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- Watchlist (users tracking items at target prices)
-- =========================================================
CREATE TABLE watchlist (
    watch_id        SERIAL PRIMARY KEY,
    user_id         INT REFERENCES users(user_id) ON DELETE CASCADE,
    item_id         INT REFERENCES items(item_id) ON DELETE CASCADE,
    target_price    NUMERIC(10,2),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, item_id) -- prevent duplicates
);

-- =========================================================
-- Transactions (completed sales)
-- =========================================================
CREATE TABLE transactions (
    transaction_id   SERIAL PRIMARY KEY,
    buyer_id         INT REFERENCES users(user_id) ON DELETE CASCADE,
    seller_id        INT REFERENCES users(user_id) ON DELETE CASCADE,
    item_id          INT REFERENCES items(item_id) ON DELETE CASCADE,
    sale_price       NUMERIC(10,2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- Messages (buyer ↔ seller communication)
-- =========================================================
CREATE TABLE messages (
    message_id      SERIAL PRIMARY KEY,
    sender_id       INT REFERENCES users(user_id) ON DELETE CASCADE,
    receiver_id     INT REFERENCES users(user_id) ON DELETE CASCADE,
    item_id         INT REFERENCES items(item_id) ON DELETE CASCADE,
    content         TEXT NOT NULL,
    sent_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- Favorites (favorite sellers/buyers)
-- =========================================================
CREATE TABLE favorites (
    favorite_id      SERIAL PRIMARY KEY,
    user_id          INT REFERENCES users(user_id) ON DELETE CASCADE,
    favorite_user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, favorite_user_id)
);

-- =========================================================
-- Sample Data (optional for testing)
-- =========================================================
INSERT INTO users (first_name, last_name, username, email, password_hash, city, state)
VALUES
('Michael', 'Rios', 'mrios', 'mrios@example.com', 'hashed_pw1', 'Victoria', 'TX'),
('Emily', 'Gallegos', 'egallegos', 'egallegos@example.com', 'hashed_pw2', 'Austin', 'TX'),
('John', 'Smith', 'jsmith', 'jsmith@example.com', 'hashed_pw3', 'Dallas', 'TX');

INSERT INTO items (seller_id, title, description, category, price)
VALUES
(1, 'Gaming Laptop', 'High performance laptop with RTX GPU', 'Electronics', 1200.00),
(2, 'Mountain Bike', 'Lightweight aluminum frame, 21-speed', 'Sports', 450.00),
(3, 'Smartphone', 'Latest model with OLED display', 'Electronics', 800.00);

INSERT INTO watchlist (user_id, item_id, target_price)
VALUES
(3, 1, 1000.00), -- John watching Michael's laptop
(1, 2, 400.00);  -- Michael watching Emily's bike
