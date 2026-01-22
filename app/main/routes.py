# Student ID: 24071105
# Student Name: Riya Adhikari

from flask import Blueprint, render_template
from app.models import Hotel, Currency
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    cities = Hotel.get_all_cities()
    currencies = Currency.get_all()
    return render_template('main/index.html', cities=cities, currencies=currencies)

@main.route('/privacy')
def privacy():
    return render_template('privacy.html', now=datetime.now())
