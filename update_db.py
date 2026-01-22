# Student ID: 24071105
# Student Name: Riya Adhikari

from app import create_app
from app.db import get_db

app = create_app()

with app.app_context():
    db = get_db()
    cursor = db.cursor()
    
    print("Checking for currencies table...")
    cursor.execute("SHOW TABLES LIKE 'currencies'")
    result = cursor.fetchone()
    
    if not result:
        print("Creating currencies table...")
        sql = """
        CREATE TABLE currencies (
            currency_code VARCHAR(3) PRIMARY KEY,
            currency_name VARCHAR(50) NOT NULL,
            symbol VARCHAR(5) NOT NULL,
            exchange_rate DECIMAL(10, 4) NOT NULL DEFAULT 1.0000
        );
        """
        cursor.execute(sql)
        
        print("Seeding currencies...")
        seed_sql = """
        INSERT INTO currencies (currency_code, currency_name, symbol, exchange_rate) VALUES
        ('GBP', 'British Pound', '£', 1.0000),
        ('USD', 'US Dollar', '$', 1.2700),
        ('EUR', 'Euro', '€', 1.1600);
        """
        cursor.execute(seed_sql)
        db.commit()
        print("Done.")
    else:
        print("Currencies table already exists.")
