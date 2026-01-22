-- Seed Data
-- Student ID: 24071105
-- Student Name: Riya Adhikari

-- Insert Room Types
INSERT INTO room_types (type_name, base_occupancy, max_occupancy) VALUES
('Standard', 1, 1),
('Double', 1, 2), -- Can be 1 or 2 guests
('Family', 1, 4); -- Assume base is 1 for pricing calculation logic, max 4

-- Insert Hotels (Data from Table 1)
-- City | Capacity | Peak £ | Off-Peak £
INSERT INTO hotels (city, total_capacity, peak_rate, off_peak_rate) VALUES
('Aberdeen', 90, 140.00, 70.00),
('Belfast', 80, 130.00, 70.00),
('Birmingham', 110, 150.00, 75.00),
('Bristol', 100, 140.00, 70.00),
('Cardiff', 90, 130.00, 70.00),
('Edinburgh', 120, 160.00, 80.00),
('Glasgow', 140, 150.00, 75.00),
('London', 160, 200.00, 100.00),
('Manchester', 150, 180.00, 90.00),
('New Castle', 90, 120.00, 70.00),
('Norwich', 90, 130.00, 70.00),
('Nottingham', 110, 130.00, 70.00),
('Oxford', 90, 180.00, 90.00),
('Plymouth', 80, 180.00, 90.00),
('Swansea', 70, 130.00, 70.00),
('Bournemouth', 90, 130.00, 70.00),
('Kent', 100, 140.00, 80.00);

-- Insert Currencies
INSERT INTO currencies (currency_code, currency_name, symbol, exchange_rate) VALUES
('GBP', 'British Pound', '£', 1.0000),
('USD', 'US Dollar', '$', 1.2700),
('EUR', 'Euro', '€', 1.1600);

-- Insert Admin User (Password needs to be hashed in real app)
-- INSERT INTO users (username, email, password_hash, role) VALUES ...
