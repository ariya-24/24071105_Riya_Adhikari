# Student ID: 24071105
# Student Name: Riya Adhikari

import os
from app.db import get_db
from app.models import User

def auto_setup(app):
    """
    Run schema, seed, and admin creation only if the admin user does not exist.
    """
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # Check if users table exists
        cursor.execute("SHOW TABLES LIKE 'users'")
        users_table_exists = cursor.fetchone()

        if users_table_exists:
            # If table exists, check for admin user
            cursor.execute("SELECT * FROM users WHERE email = 'admin@wh.com'")
            if cursor.fetchone():
                return  # Already set up

        # Run schema.sql (creates tables if not present)
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema = f.read()
        for statement in schema.split(';'):
            if statement.strip():
                try:
                    cursor.execute(statement)
                except Exception:
                    pass  # Ignore errors if table already exists

        # Run seed_data.sql
        seed_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'seed_data.sql')
        with open(seed_path, 'r') as f:
            seed = f.read()
        for statement in seed.split(';'):
            if statement.strip():
                try:
                    cursor.execute(statement)
                except Exception:
                    pass  # Ignore errors if data already exists

        # Create admin user
        if User.create('admin', 'admin@wh.com', 'admin123'):
            cursor.execute("UPDATE users SET role = 'admin' WHERE email = 'admin@wh.com'")
        db.commit()
