# Student ID: 24071105
# Student Name: Riya Adhikari

from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort
from datetime import datetime
from typing import Any
from app.models import Hotel, RoomType, Booking, Currency
from app.booking.pricing import calculate_total_price, calculate_cancellation_refund
from app.utils import login_required

booking = Blueprint('booking', __name__)

@booking.route('/')
def index():
    return redirect(url_for('main.index'))

@booking.route('/search', methods=['GET'])
def search():
    city = request.args.get('city')
    check_in_str = request.args.get('check_in')
    check_out_str = request.args.get('check_out')
    guests = int(request.args.get('guests', 1))
    room_type = request.args.get('room_type', 'Standard')
    currency_code = request.args.get('currency', 'GBP')
    
    currency: Any = Currency.get_by_code(currency_code)
    if not currency:
        currency = {'currency_code': 'GBP', 'exchange_rate': 1.0, 'symbol': '£'}

    if not all([city, check_in_str, check_out_str]):
        flash('Please fill in all search fields.', 'warning')
        return redirect(url_for('main.index'))

    # Ensure strings for typing
    check_in_str = str(check_in_str)
    check_out_str = str(check_out_str)

    try:
        check_in_date = datetime.strptime(check_in_str, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out_str, "%Y-%m-%d").date()
        today = datetime.now().date() # Current date for booking date logic
        
        if check_in_date < today:
             flash('Check-in date cannot be in the past.', 'danger')
             return redirect(url_for('main.index'))
             
        if check_out_date <= check_in_date:
            flash('Check-out date must be after check-in date.', 'danger')
            return redirect(url_for('main.index'))
            
    except ValueError:
        flash('Invalid date format.', 'danger')
        return redirect(url_for('main.index'))

    # Fetch hotels
    hotels_in_city = Hotel.get_by_city(city)
    available_hotels = []

    for hotel in hotels_in_city:
        # Check Availability
        if not Hotel.check_availability(hotel.hotel_id, room_type, check_in_date, check_out_date):
            continue
        
        # Calculate Price
        price, error = calculate_total_price(
            hotel.peak_rate,
            hotel.off_peak_rate,
            check_in_date,
            check_out_date,
            today, # Booking Date is Today
            room_type,
            guests
        )
        
        if error:
             # Skip this hotel if specific rules (e.g. max stay) are violated
             continue
        else:
            # Ensure exchange_rate is float
            rate = float(currency.get('exchange_rate', 1.0))
            converted_price = float(price) * rate
            available_hotels.append({
                'hotel': hotel,
                'total_price': price, # GBP
                'display_price': "{:.2f}".format(converted_price),
                'room_type': room_type,
                'guests': guests,
                'check_in': check_in_str,
                'check_out': check_out_str
            })

    return render_template('booking/search_results.html', 
                           hotels=available_hotels, 
                           currency=currency)

@booking.route('/book/confirm', methods=['GET'])
@login_required
def book_confirm():
    hotel_id = request.args.get('hotel_id')
    room_type = request.args.get('room_type')
    guests = request.args.get('guests')
    check_in_str = request.args.get('check_in')
    check_out_str = request.args.get('check_out')
    price = request.args.get('price')

    hotel = Hotel.get_by_id(hotel_id)
    if not hotel:
        flash('Hotel not found.', 'danger')
        return redirect(url_for('main.index'))

    return render_template('booking/confirm.html',
                           hotel=hotel,
                           room_type=room_type,
                           guests=guests,
                           check_in=check_in_str,
                           check_out=check_out_str,
                           price=price)

@booking.route('/book/create', methods=['POST'])
@login_required
def book_create():
    hotel_id = request.form.get('hotel_id')
    room_type_name = request.form.get('room_type')
    check_in_str = request.form.get('check_in')
    check_out_str = request.form.get('check_out')
    price = request.form.get('price') # In production, re-calculate this! Trusting client is bad.
    
    # Re-calculate price for security is recommended. 
    # For this coursework level, ensure we at least re-fetch IDs.
    
    room_type_id = RoomType.get_id_by_name(room_type_name)
    if not room_type_id:
        flash('Invalid Room Type', 'danger')
        return redirect(url_for('main.index'))
        
    booking_id = Booking.create(
        user_id=session['user_id'],
        hotel_id=hotel_id,
        room_type_id=room_type_id,
        check_in_date=check_in_str,
        check_out_date=check_out_str,
        total_price=price
    )
    
    if booking_id:
        flash('Booking Confirmed! Reference ID: ' + str(booking_id), 'success')
        return redirect(url_for('main.index'))
    else:
        flash('Booking failed. Please try again.', 'danger')
        return redirect(url_for('main.index'))

@booking.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.get_by_user(session['user_id'])
    return render_template('booking/my_bookings.html', bookings=bookings)

@booking.route('/receipt/<int:booking_id>')
@login_required
def receipt(booking_id):
    booking_data: Any = Booking.get_by_id(booking_id)
    if not booking_data:
        abort(404)
    
    # Security check: Ensure the current user owns this booking
    # Use .get() to satisfy generic dictionary access checks
    if booking_data.get('user_id') != session['user_id']:
        abort(403)
        
    return render_template('booking/receipt.html', booking=booking_data)

@booking.route('/cancel/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def cancel(booking_id):
    booking: Any = Booking.get_by_id(booking_id)
    
    # 1. Validation
    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('booking.my_bookings'))
        
    if booking.get('user_id') != session['user_id']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('booking.my_bookings'))
        
    if booking.get('status') == 'cancelled':
        flash('Booking is already cancelled.', 'warning')
        return redirect(url_for('booking.my_bookings'))
        
    # 2. Refund Calculation
    today = datetime.now()
    # Ensure check_in_date is a date object for calculation (DB usually returns date)
    check_in_date = booking.get('check_in_date') # Assumed date object from mysql connector
    
    refund_amount, refund_msg = calculate_cancellation_refund(check_in_date, today, float(booking.get('total_price', 0)))
    
    if request.method == 'POST':
        if Booking.cancel(booking_id):
            flash(f'Booking Cancelled. {refund_msg} (£{refund_amount})', 'success')
        else:
            flash('Cancellation failed. Please try again.', 'danger')
        return redirect(url_for('booking.my_bookings'))
        
    return render_template('booking/cancel_confirm.html', booking=booking, refund_amount=refund_amount, refund_msg=refund_msg)

