from models.user import User
from models.turf import Turf
from models.turf_slot import TurfSlot
from models.booking import Booking
from models import session
from datetime import datetime

def exit_program():
    print("Goodbye!")
    exit()

# User helpers
def list_users():
    users = User.get_all(session)
    for user in users:
        print(user)

def find_user_by_email():
    email = input("Enter the user's email: ")
    user = User.find_by_email(session, email)
    print(user) if user else print(f'User {email} not found')

def find_user_by_id():
    id_ = input("Enter the user's id: ")
    user = User.find_by_id(session, id_)
    print(user) if user else print(f'User {id_} not found')

def create_user():
    email = input("Enter the user's email: ")
    password_hash = input("Enter the password hash: ")
    role = input("Enter the role (default: player): ") or 'player'
    city = input("Enter the city: ")
    try:
        user = User.create(session, email, password_hash, role, city)
        print(f'Success: {user}')
    except Exception as exc:
        print("Error creating user: ", exc)

def update_user():
    id_ = input("Enter the user's id: ")
    if user := User.find_by_id(session, id_):
        try:
            email = input("Enter the new email: ")
            if email:
                user.email = email
            password_hash = input("Enter the new password hash: ")
            if password_hash:
                user.password_hash = password_hash
            role = input("Enter the new role: ")
            if role:
                user.role = role
            city = input("Enter the new city: ")
            if city:
                user.city = city
            user.update(session)
            print(f'Success: {user}')
        except Exception as exc:
            print("Error updating user: ", exc)
    else:
        print(f'User {id_} not found')

def delete_user():
    id_ = input("Enter the user's id: ")
    if user := User.find_by_id(session, id_):
        user.delete(session)
        print(f'User {id_} deleted')
    else:
        print(f'User {id_} not found')

# Turf helpers
def list_turfs():
    turfs = Turf.get_all(session)
    for turf in turfs:
        print(turf)

def find_turf_by_name():
    name = input("Enter the turf's name: ")
    turf = Turf.find_by_name(session, name)
    print(turf) if turf else print(f'Turf {name} not found')

def find_turf_by_id():
    id_ = input("Enter the turf's id: ")
    turf = Turf.find_by_id(session, id_)
    print(turf) if turf else print(f'Turf {id_} not found')

def create_turf():
    name = input("Enter the turf's name: ")
    city = input("Enter the city: ")
    latitude = input("Enter latitude (optional): ")
    longitude = input("Enter longitude (optional): ")
    base_price_per_hour = float(input("Enter base price per hour: "))
    is_active = int(input("Is active (1 for yes, 0 for no, default 1): ") or 1)
    try:
        turf = Turf.create(session, name, city, float(latitude) if latitude else None, float(longitude) if longitude else None, base_price_per_hour, is_active)
        print(f'Success: {turf}')
    except Exception as exc:
        print("Error creating turf: ", exc)

def update_turf():
    id_ = input("Enter the turf's id: ")
    if turf := Turf.find_by_id(session, id_):
        try:
            name = input("Enter the new name: ")
            if name:
                turf.name = name
            city = input("Enter the new city: ")
            if city:
                turf.city = city
            latitude = input("Enter the new latitude: ")
            if latitude:
                turf.latitude = float(latitude)
            longitude = input("Enter the new longitude: ")
            if longitude:
                turf.longitude = float(longitude)
            base_price_per_hour = input("Enter the new base price per hour: ")
            if base_price_per_hour:
                turf.base_price_per_hour = float(base_price_per_hour)
            is_active = input("Is active (1 or 0): ")
            if is_active:
                turf.is_active = int(is_active)
            turf.update(session)
            print(f'Success: {turf}')
        except Exception as exc:
            print("Error updating turf: ", exc)
    else:
        print(f'Turf {id_} not found')

def delete_turf():
    id_ = input("Enter the turf's id: ")
    if turf := Turf.find_by_id(session, id_):
        turf.delete(session)
        print(f'Turf {id_} deleted')
    else:
        print(f'Turf {id_} not found')

# Turf Slot helpers
def list_turf_slots():
    slots = TurfSlot.get_all(session)
    for slot in slots:
        print(slot)

def find_turf_slot_by_id():
    id_ = input("Enter the turf slot's id: ")
    slot = TurfSlot.find_by_id(session, id_)
    print(slot) if slot else print(f'Turf slot {id_} not found')

def create_turf_slot():
    turf_id = input("Enter the turf id: ")
    slot_date = input("Enter slot date (YYYY-MM-DD): ")
    start_time = input("Enter start time (HH:MM): ")
    end_time = input("Enter end time (HH:MM): ")
    final_price = float(input("Enter final price: "))
    status = input("Enter status (default: available): ") or 'available'
    try:
        slot = TurfSlot.create(session, turf_id, datetime.strptime(slot_date, '%Y-%m-%d').date(), start_time, end_time, final_price, status)
        print(f'Success: {slot}')
    except Exception as exc:
        print("Error creating turf slot: ", exc)

def update_turf_slot():
    id_ = input("Enter the turf slot's id: ")
    if slot := TurfSlot.find_by_id(session, id_):
        try:
            turf_id = input("Enter the new turf id: ")
            if turf_id:
                slot.turf_id = turf_id
            slot_date = input("Enter the new slot date (YYYY-MM-DD): ")
            if slot_date:
                slot.slot_date = datetime.strptime(slot_date, '%Y-%m-%d').date()
            start_time = input("Enter the new start time: ")
            if start_time:
                slot.start_time = start_time
            end_time = input("Enter the new end time: ")
            if end_time:
                slot.end_time = end_time
            final_price = input("Enter the new final price: ")
            if final_price:
                slot.final_price = float(final_price)
            status = input("Enter the new status: ")
            if status:
                slot.status = status
            slot.update(session)
            print(f'Success: {slot}')
        except Exception as exc:
            print("Error updating turf slot: ", exc)
    else:
        print(f'Turf slot {id_} not found')

def delete_turf_slot():
    id_ = input("Enter the turf slot's id: ")
    if slot := TurfSlot.find_by_id(session, id_):
        slot.delete(session)
        print(f'Turf slot {id_} deleted')
    else:
        print(f'Turf slot {id_} not found')

# Booking helpers
def list_bookings():
    bookings = Booking.get_all(session)
    for booking in bookings:
        print(booking)

def find_booking_by_id():
    id_ = input("Enter the booking's id: ")
    booking = Booking.find_by_id(session, id_)
    print(booking) if booking else print(f'Booking {id_} not found')

def create_booking():
    turf_id = input("Enter the turf id: ")
    slot_id = input("Enter the slot id: ")
    user_id = input("Enter the user id: ")
    booking_date = input("Enter booking date (YYYY-MM-DD): ")
    total_amount = float(input("Enter total amount: "))
    status = input("Enter status (default: pending): ") or 'pending'
    try:
        booking = Booking.create(session, turf_id, slot_id, user_id, datetime.strptime(booking_date, '%Y-%m-%d').date(), total_amount, status)
        print(f'Success: {booking}')
    except Exception as exc:
        print("Error creating booking: ", exc)

def update_booking():
    id_ = input("Enter the booking's id: ")
    if booking := Booking.find_by_id(session, id_):
        try:
            turf_id = input("Enter the new turf id: ")
            if turf_id:
                booking.turf_id = turf_id
            slot_id = input("Enter the new slot id: ")
            if slot_id:
                booking.slot_id = slot_id
            user_id = input("Enter the new user id: ")
            if user_id:
                booking.user_id = user_id
            booking_date = input("Enter the new booking date (YYYY-MM-DD): ")
            if booking_date:
                booking.booking_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
            total_amount = input("Enter the new total amount: ")
            if total_amount:
                booking.total_amount = float(total_amount)
            status = input("Enter the new status: ")
            if status:
                booking.status = status
            booking.update(session)
            print(f'Success: {booking}')
        except Exception as exc:
            print("Error updating booking: ", exc)
    else:
        print(f'Booking {id_} not found')

def delete_booking():
    id_ = input("Enter the booking's id: ")
    if booking := Booking.find_by_id(session, id_):
        booking.delete(session)
        print(f'Booking {id_} deleted')
    else:
        print(f'Booking {id_} not found')
