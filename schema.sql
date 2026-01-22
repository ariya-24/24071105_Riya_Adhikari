-- Schema initialization
-- Student ID: 24071105
-- Student Name: Riya Adhikari

/*
NORMALIZATION DOCUMENTATION (3NF Compliance)

1. First Normal Form (1NF):
   - All columns contain atomic values (no lists of phone numbers or dates).
   - Each table has a primary key (user_id, hotel_id, etc.).
   - No repeating groups (e.g., we don't not have Hotel_Room1, Hotel_Room2 columns).

2. Second Normal Form (2NF):
   - All tables are in 1NF.
   - All non-key attributes are fully dependent on the Primary Key.
   - Example: In 'hotels' table, 'peak_rate' depends entirely on 'hotel_id'. 
   - We separated 'bookings' from 'hotels' so booking details (dates) depend on 'booking_id', not mixed with hotel info.

3. Third Normal Form (3NF):
   - All tables are in 2NF.
   - No transitive dependencies (non-key attributes depending on other non-key attributes).
   - Example: 'room_types' is a separate table. We do not store 'base_occupancy' in the 'bookings' table, 
     which would depend on 'room_type_id' (a non-key attribute in bookings). 
     Instead, we reference 'room_type_id' as a Foreign Key.
*/

-- Drop tables if they exist to start fresh (Order matters for Foreign Keys)
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS room_types;
DROP TABLE IF EXISTS hotels;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS currencies;

-- 1. Users Table (Admin, Customers)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'customer') DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Hotels Table
CREATE TABLE hotels (
    hotel_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    total_capacity INT NOT NULL,
    peak_rate DECIMAL(10, 2) NOT NULL,
    off_peak_rate DECIMAL(10, 2) NOT NULL
);

-- 3. Rooms Table

CREATE TABLE room_types (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name ENUM('Standard', 'Double', 'Family') NOT NULL UNIQUE,
    base_occupancy INT NOT NULL,
    max_occupancy INT NOT NULL
);

-- 4. Bookings Table
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    hotel_id INT NOT NULL,
    room_type_id INT NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10, 2) NOT NULL,
    status ENUM('confirmed', 'cancelled') DEFAULT 'confirmed',
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id),
    FOREIGN KEY (room_type_id) REFERENCES room_types(type_id)
);

-- 5. Currencies Table
CREATE TABLE currencies (
    currency_code VARCHAR(3) PRIMARY KEY,
    currency_name VARCHAR(50) NOT NULL,
    symbol VARCHAR(5) NOT NULL,
    exchange_rate DECIMAL(10, 4) NOT NULL DEFAULT 1.0000
);
