# Student ID: 24071105
# Student Name: Riya Adhikari

from flask import Blueprint, render_template, redirect, url_for, flash
from app.utils import admin_required
from app.models import User, Booking, Hotel, Currency
from app.admin.forms import HotelForm, UserEditForm, CurrencyForm, UserAddForm, CurrencyAddForm

admin = Blueprint('admin', __name__)

@admin.route('/')
@admin_required
def index():
    return render_template('admin/dashboard.html')

@admin.route('/users')
@admin_required
def manage_users():
    users = User.get_all()
    return render_template('admin/users.html', users=users)

@admin.route('/user/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    form = UserAddForm()
    if form.validate_on_submit():
        if User.get_by_email(form.email.data):
             flash('Email already registered.', 'danger')
        else:
             if User.create(form.username.data, form.email.data, form.password.data, form.role.data):
                 flash('User created successfully.', 'success')
                 return redirect(url_for('admin.manage_users'))
             else:
                 flash('Error creating user.', 'danger')
    return render_template('admin/add_user.html', form=form)

@admin.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    form = UserEditForm()
    if form.validate_on_submit():
        if form.password.data:
            User.update_password(user_id, form.password.data)
            flash('Password updated successfully.', 'success')
        else:
            flash('No changes made.', 'info')
        return redirect(url_for('admin.manage_users'))
        
    return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/user/delete/<int:user_id>')
@admin_required
def delete_user(user_id):
    # Prevent deleting yourself
    if user_id == session.get('user_id'):
        flash('You cannot delete your own admin account.', 'danger')
        return redirect(url_for('admin.manage_users'))
        
    if User.delete(user_id):
        flash('User deleted.', 'success')
    else:
        flash('Error deleting user.', 'danger')
    return redirect(url_for('admin.manage_users'))

@admin.route('/currencies', methods=['GET', 'POST'])
@admin_required
def manage_currencies():
    currencies = Currency.get_all()
    # Handle inline updates or clicking edit?
    # Simple approach: List them, click "Edit" to go to form.
    return render_template('admin/currencies.html', currencies=currencies)

@admin.route('/currency/add', methods=['GET', 'POST'])
@admin_required
def add_currency():
    form = CurrencyAddForm()
    if form.validate_on_submit():
        if Currency.get_by_code(form.currency_code.data):
             flash(f'Currency {form.currency_code.data} already exists.', 'danger')
        elif Currency.create(form.currency_code.data.upper(), form.currency_name.data, form.symbol.data, form.exchange_rate.data):
             flash('Currency added successfully.', 'success')
             return redirect(url_for('admin.manage_currencies'))
        else:
             flash('Error adding currency.', 'danger')
    return render_template('admin/add_currency.html', form=form)

@admin.route('/currency/edit/<code>', methods=['GET', 'POST'])
@admin_required
def edit_currency(code):
    currency = Currency.get_by_code(code)
    if not currency:
       flash('Currency not found', 'danger')
       return redirect(url_for('admin.manage_currencies'))
       
    form = CurrencyForm(data={'exchange_rate': currency['exchange_rate']})
    if form.validate_on_submit():
        if Currency.update_rate(code, form.exchange_rate.data):
             flash('Rate updated.', 'success')
             return redirect(url_for('admin.manage_currencies'))
        else:
             flash('Error updating rate.', 'danger')
             
    return render_template('admin/edit_currency.html', form=form, currency=currency)

@admin.route('/hotels')
@admin_required
def manage_hotels():
    hotels = Hotel.get_all()
    return render_template('admin/hotels.html', hotels=hotels)

@admin.route('/hotel/edit/<int:hotel_id>', methods=['GET', 'POST'])
@admin_required
def edit_hotel(hotel_id):
    hotel = Hotel.get_by_id(hotel_id)
    if not hotel:
        flash('Hotel not found.', 'danger')
        return redirect(url_for('admin.manage_hotels'))
    
    form = HotelForm(obj=hotel) 
    # Note: 'obj=hotel' populates form if fields match attribute names. 
    # Our Hotel model has same attribute names as form fields :)
    
    if form.validate_on_submit():
        if Hotel.update(hotel_id, form.total_capacity.data, form.peak_rate.data, form.off_peak_rate.data):
             flash(f'Hotel {hotel.city} updated successfully.', 'success')
             return redirect(url_for('admin.manage_hotels'))
        else:
             flash('Update failed.', 'danger')
             
    return render_template('admin/edit_hotel.html', form=form, hotel=hotel)

@admin.route('/reports')
@admin_required
def reports():
    sales = Booking.get_sales_report()
    return render_template('admin/reports.html', sales=sales)

@admin.route('/bookings')
@admin_required
def manage_bookings():
    bookings = Booking.get_all()
    return render_template('admin/bookings.html', bookings=bookings)

@admin.route('/booking/cancel/<int:booking_id>')
@admin_required
def cancel_booking(booking_id):
    if Booking.cancel(booking_id):
        flash('Booking cancelled successfully.', 'success')
    else:
        flash('Failed to cancel booking.', 'danger')
    return redirect(url_for('admin.manage_bookings'))
