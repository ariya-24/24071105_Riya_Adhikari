# Student ID: 24071105
# Student Name: Riya Adhikari

from app import create_app
from app.db import get_db

app = create_app()

with app.app_context():
    db = get_db()
    cursor = db.cursor()
    
    # Read schema.sql
    with open('schema.sql', 'r') as f:
        schema = f.read()
        
    # Execute schema (split by ;)
    print("Resetting database...")
    for statement in schema.split(';'):
        if statement.strip():
            cursor.execute(statement)
            
    # Read seed_data.sql
    with open('seed_data.sql', 'r') as f:
        seed = f.read()
        
    # Execute seed
    print("Seeding database...")
    for statement in seed.split(';'):
        if statement.strip():
            cursor.execute(statement)
            
    db.commit()
    print("Database reset and seeded successfully.")
