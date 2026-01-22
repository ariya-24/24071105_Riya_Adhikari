# Student ID: 24071105
# Student Name: Riya Adhikari

from datetime import datetime, date

def is_peak_season(check_in_date):
    """
    Determines if the check-in date falls in a peak season.
    Peak Seasons: April-August (4-8) and November-December (11-12).
    """
    month = check_in_date.month
    if 4 <= month <= 8 or 11 <= month <= 12:
        return True
    return False

def calculate_room_multiplier(room_type, guests):
    """
    Calculates the price multiplier based on room type and number of guests.
    Standard: Base Rate (1 guest max) -> 1.0
    Double:
        - 1 Guest: Base Rate + 20% -> 1.2
        - 2 Guests: Base Rate + 20% + 10% -> 1.3
    Family: Base Rate + 50% (4 guests max) -> 1.5
    """
    room_type = room_type.lower()
    if room_type == 'standard':
        return 1.0
    elif room_type == 'double':
        if guests == 1:
            return 1.2
        elif guests == 2:
            return 1.3
    elif room_type == 'family':
        return 1.5
    
    # Default fallback (should ideally raise error or validation before this)
    return 1.0

def get_advance_booking_discount(booking_date, check_in_date):
    """
    Calculates discount percentage based on how many days in advance the booking is made.
    80 - 90 days: 30% (0.30)
    60 - 79 days: 20% (0.20)
    45 - 59 days: 10% (0.10)
    < 45 days: 0%
    Max booking window: 90 days.
    """
    if isinstance(booking_date, datetime):
        booking_date = booking_date.date()
    if isinstance(check_in_date, datetime):
        check_in_date = check_in_date.date()
        
    delta = (check_in_date - booking_date).days
    
    if delta > 90:
        return 0, "Booking dates beyond 90 days are not allowed." # Or handle validation elsewhere
    if 80 <= delta <= 90:
        return 0.30, None
    elif 60 <= delta <= 79:
        return 0.20, None
    elif 45 <= delta <= 59:
        return 0.10, None
    else:
        return 0.0, None

def calculate_total_price(base_rate_peak, base_rate_off_peak, check_in_date, check_out_date, booking_date, room_type, guests):
    """
    Calculates the total price for the stay.
    Note: 'Peak Seasons (Check-in date)' implies the rate is determined by the check-in date for the whole stay?
    Brief says: "Peak Seasons (Check-in date): ...". Usually in hotels, it's per night.
    However, simplest interpretation of 'Peak Seasons (Check-in date)' is that the Check-in date determines the season for the rate lookup.
    Let's assume the rate is constant for the stay based on check-in date season, 
    OR we check per night. 
    The Hotel Data has 'Peak £' and 'Off-Peak £'.
    Let's interpret 'Peak Seasons (Check-in date)' as: "If check-in date is in peak months, use Peak Rate, else Off-Peak Rate".
    """
    
    # 1. Determine Base Rate (Peak vs Off-Peak)
    if is_peak_season(check_in_date):
        base_rate = float(base_rate_peak)
    else:
        base_rate = float(base_rate_off_peak)
        
    # 2. Apply Room Type & Guest Multiplier
    multiplier = calculate_room_multiplier(room_type, guests)
    adjusted_nightly_rate = base_rate * multiplier
    
    # 3. Calculate Number of Nights
    if isinstance(check_in_date, datetime):
        check_in_date = check_in_date.date()
    if isinstance(check_out_date, datetime):
        check_out_date = check_out_date.date()
        
    num_nights = (check_out_date - check_in_date).days
    
    if num_nights < 1:
        return 0, "Invalid dates"
    if num_nights > 30:
        return 0, "Stay cannot exceed 30 days"

    total_gross = adjusted_nightly_rate * num_nights
    
    # 4. Apply Advanced Booking Discount
    discount_percent, error = get_advance_booking_discount(booking_date, check_in_date)
    if error:
        return 0, error
        
    discount_amount = total_gross * discount_percent
    final_price = total_gross - discount_amount
    
    return round(final_price, 2), None

def calculate_cancellation_refund(check_in_date, cancellation_date, total_price):
    """
    Calculates the refund amount based on cancellation policy.
    - > 60 days before: Free cancellation (100% refund).
    - 30 - 60 days before: 50% charge (50% refund).
    - < 30 days before: 100% charge (No refund).
    """
    if isinstance(check_in_date, datetime):
        check_in_date = check_in_date.date()
    if isinstance(cancellation_date, datetime):
        cancellation_date = cancellation_date.date()
        
    delta = (check_in_date - cancellation_date).days
    
    total_price = float(total_price)
    
    if delta > 60:
        return total_price, "100% Refund"
    elif 30 <= delta <= 60:
        return total_price * 0.5, "50% Refund"
    else:
        return 0.0, "No Refund"
