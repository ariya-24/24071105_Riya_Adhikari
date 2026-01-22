World Hotels (WH) Booking System
--------------------------------
Student ID: 24071105
Student Name: Riya Adhikari

1. Setup Instructions
---------------------
Prerequisites: Python 3.7+, MySQL Server.

a. Create a MySQL database (e.g., 'wh_booking').
b. Configure database connection in `config.py` (Update DB_USER, DB_PASSWORD if necessary).
c. Install dependencies:
   pip install -r requirements.txt
d. Initialize Database:
   python reset_db.py
   (This runs schema.sql and seed_data.sql)

e. Create Admin User:
   python create_admin.py

f. Run Application:
   python run.py
   Access at http://127.0.0.1:5000

2. Credentials
--------------------
Admin User:
  Email: admin@wh.com
  Password: admin123

Standard User:
  Email: reya@wh.com
  Password: reya123

3. Project Structure
--------------------
- app/: Main Flask application package
  - auth/: Authentication blueprint
  - booking/: Booking & Pricing blueprint
  - admin/: Admin management blueprint
  - main/: Public routes blueprint
- schema.sql: Database schema definitions (3NF)
- seed_data.sql: Initial hotel and room type data
- PROJECT_PLAN.md: Roadmap and Checklist
