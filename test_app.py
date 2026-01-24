# test_app.py

import pytest
from app import create_app

def test_homepage():
    app = create_app()
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_login_logout():
    app = create_app()
    client = app.test_client()
    # Register a user
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123',
        'submit': True
    }, follow_redirects=True)
    # Login
    response = client.post('/auth/login', data={
        'email': 'testuser@example.com',
        'password': 'testpass123',
        'submit': True
    }, follow_redirects=True)
    assert b'Logged in successfully.' in response.data
    # Logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert b'You have been logged out.' in response.data

def test_booking_search():
    app = create_app()
    client = app.test_client()
    # Simulate a search (assuming test data exists)
    response = client.get('/booking/search?city=London&check_in=2026-02-01&check_out=2026-02-05&guests=1&room_type=Standard&currency=GBP')
    assert response.status_code == 200
    assert b'Hotels' in response.data or b'hotel' in response.data
