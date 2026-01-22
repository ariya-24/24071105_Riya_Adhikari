# Student ID: 24071105
# Student Name: Riya Adhikari

from app.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from typing import Any

class User:
    def __init__(self, user_id, username, email, role):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.role = role

    @staticmethod
    def create(username, email, password, role='customer'):
        """Create a new user in the database."""
        db = get_db()
        cursor = db.cursor()
        password_hash = generate_password_hash(password)
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                (username, email, password_hash, role)
            )
            db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}") # In production, log this
            return False
        finally:
            cursor.close()

    @staticmethod
    def get_by_email(email):
        """Fetch a user by email."""
        db = get_db()
        cursor = db.cursor(dictionary=True) # Return results as dictionaries
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user: Any = cursor.fetchone()
            if user:
                return User(
                    user_id=user.get('user_id'),
                    username=user.get('username'),
                    email=user.get('email'),
                    role=user.get('role')
                )
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(user_id):
        """Fetch a user by ID."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user: Any = cursor.fetchone()
            if user:
                return User(
                    user_id=user.get('user_id'),
                    username=user.get('username'),
                    email=user.get('email'),
                    role=user.get('role')
                )
            return None
        finally:
            cursor.close()

    @staticmethod
    def update_password(user_id, new_password):
        """Update user password (re-hash)."""
        password_hash = generate_password_hash(new_password)
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE users SET password_hash = %s WHERE user_id = %s", (password_hash, user_id))
            db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(user_id):
        """Delete a user and their bookings."""
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM bookings WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def check_password(email, password):
        """Verify password for a given email."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
            user: Any = cursor.fetchone()
            if user and check_password_hash(user.get('password_hash'), password):
                return True
            return False
        finally:
            cursor.close()

    @staticmethod
    def get_all():
        """Fetch all users."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
            return cursor.fetchall()
        finally:
            cursor.close()

class Hotel:
    def __init__(self, hotel_id, city, total_capacity, peak_rate, off_peak_rate):
        self.hotel_id = hotel_id
        self.city = city
        self.total_capacity = total_capacity
        self.peak_rate = peak_rate
        self.off_peak_rate = off_peak_rate

    @staticmethod
    def get_all_cities():
        """Fetch unique cities for the dropdown."""
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT DISTINCT city FROM hotels ORDER BY city")
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()

    @staticmethod
    def get_by_city(city):
        """Fetch hotels in a specific city."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM hotels WHERE city = %s", (city,))
            hotels = []
            rows: Any = cursor.fetchall()
            for row in rows:
                hotels.append(Hotel(
                    hotel_id=row['hotel_id'],
                    city=row['city'],
                    total_capacity=row['total_capacity'],
                    peak_rate=row['peak_rate'],
                    off_peak_rate=row['off_peak_rate']
                ))
            return hotels
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(hotel_id):
        """Fetch a single hotel by ID."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM hotels WHERE hotel_id = %s", (hotel_id,))
            row: Any = cursor.fetchone()
            if row:
                return Hotel(
                    hotel_id=row['hotel_id'],
                    city=row['city'],
                    total_capacity=row['total_capacity'],
                    peak_rate=row['peak_rate'],
                    off_peak_rate=row['off_peak_rate']
                )
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_all():
        """Fetch all hotels."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM hotels ORDER BY city")
            hotels = []
            rows: Any = cursor.fetchall()
            for row in rows:
                hotels.append(Hotel(
                    hotel_id=row['hotel_id'],
                    city=row['city'],
                    total_capacity=row['total_capacity'],
                    peak_rate=row['peak_rate'],
                    off_peak_rate=row['off_peak_rate']
                ))
            return hotels
        finally:
            cursor.close()

    @staticmethod
    def check_availability(hotel_id, room_type_name, check_in_val, check_out_val):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT total_capacity FROM hotels WHERE hotel_id = %s", (hotel_id,))
            hotel: Any = cursor.fetchone()
            if not hotel: return False
            total_capacity = int(hotel['total_capacity'])

            allocations = {'Standard': 0.30, 'Double': 0.50, 'Family': 0.20}
            percentage = allocations.get(room_type_name, 0)
            max_rooms = int(total_capacity * percentage)

            cursor.execute("SELECT type_id FROM room_types WHERE type_name = %s", (room_type_name,))
            rt: Any = cursor.fetchone()
            if not rt: return False
            type_id = rt['type_id']

            sql = """
                SELECT COUNT(*) as count 
                FROM bookings 
                WHERE hotel_id = %s 
                AND room_type_id = %s 
                AND status = 'confirmed'
                AND check_in_date < %s 
                AND check_out_date > %s
            """
            cursor.execute(sql, (hotel_id, type_id, check_out_val, check_in_val))
            result: Any = cursor.fetchone()
            if not result:
                 return True # No bookings found
            current_bookings = result.get('count', 0)

            return current_bookings < max_rooms
        finally:
            cursor.close()

    @staticmethod
    def update(hotel_id, total_capacity, peak_rate, off_peak_rate):
        """Update hotel details."""
        db = get_db()
        cursor = db.cursor()
        try:
            sql = "UPDATE hotels SET total_capacity=%s, peak_rate=%s, off_peak_rate=%s WHERE hotel_id=%s"
            cursor.execute(sql, (total_capacity, peak_rate, off_peak_rate, hotel_id))
            db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()

class RoomType:
    @staticmethod
    def get_id_by_name(name):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT type_id FROM room_types WHERE type_name = %s", (name,))
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            cursor.close()

class Booking:
    @staticmethod
    def create(user_id, hotel_id, room_type_id, check_in_date, check_out_date, total_price):
        db = get_db()
        cursor = db.cursor()
        try:
            sql = """
                INSERT INTO bookings (user_id, hotel_id, room_type_id, check_in_date, check_out_date, total_price)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, hotel_id, room_type_id, check_in_date, check_out_date, total_price))
            db.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            
    @staticmethod
    def get_by_user(user_id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            sql = """
                SELECT b.*, h.city, rt.type_name 
                FROM bookings b
                JOIN hotels h ON b.hotel_id = h.hotel_id
                JOIN room_types rt ON b.room_type_id = rt.type_id
                WHERE b.user_id = %s
                ORDER BY b.booking_date DESC
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(booking_id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            sql = """
                SELECT b.*, h.city, rt.type_name, u.username, u.email
                FROM bookings b
                JOIN hotels h ON b.hotel_id = h.hotel_id
                JOIN room_types rt ON b.room_type_id = rt.type_id
                JOIN users u ON b.user_id = u.user_id
                WHERE b.booking_id = %s
            """
            cursor.execute(sql, (booking_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            sql = """
                SELECT b.*, h.city, rt.type_name, u.username, u.email
                FROM bookings b
                JOIN hotels h ON b.hotel_id = h.hotel_id
                JOIN room_types rt ON b.room_type_id = rt.type_id
                JOIN users u ON b.user_id = u.user_id
                ORDER BY b.booking_date DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def cancel(booking_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE bookings SET status = 'cancelled' WHERE booking_id = %s", (booking_id,))
            db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def get_sales_report():
        """Get total sales per city."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            sql = """
                SELECT h.city, COUNT(b.booking_id) as total_bookings, SUM(b.total_price) as total_revenue
                FROM bookings b
                JOIN hotels h ON b.hotel_id = h.hotel_id
                WHERE b.status = 'confirmed'
                GROUP BY h.city
                ORDER BY total_revenue DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()

class Currency:
    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM currencies")
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def get_by_code(code):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM currencies WHERE currency_code = %s", (code,))
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    def update_rate(code, rate):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE currencies SET exchange_rate = %s WHERE currency_code = %s", (rate, code))
            db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def create(code, name, symbol, rate):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO currencies (currency_code, currency_name, symbol, exchange_rate) VALUES (%s, %s, %s, %s)",
                (code, name, symbol, rate)
            )
            db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
