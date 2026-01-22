# Student ID: 24071105
# Student Name: Riya Adhikari

from app import create_app
from app.models import User
from app.db import get_db

app = create_app()

with app.app_context():
    print("Creating admin user...")
    if not User.get_by_email('admin@wh.com'):
        # Manually create with role='admin'
        # User.create only does customer role by default usually?
        # Let's check User.create
        # It does: INSERT INTO users (username, email, password_hash) VALUES ...
        # Schema default for role is 'customer'.
        # So I need to update it or use a raw query here.
        
        # Create normal user first (handles hashing)
        if User.create('admin', 'admin@wh.com', 'admin123'):
            # Promote to admin
            db = get_db()
            cursor = db.cursor()
            cursor.execute("UPDATE users SET role = 'admin' WHERE email = 'admin@wh.com'")
            db.commit()
            print("Admin user created (admin@wh.com / admin123)")
        else:
            print("Failed to create user.")
    else:
        print("Admin user already exists.")
