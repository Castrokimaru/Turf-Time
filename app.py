from models import Session, User, Turf, TurfSlot, Booking
from datetime import date

def main():
    session = Session()

    # Create a user
    user = User.create(session, email='user@example.com', password_hash='hashedpass', city='Nairobi')
    print(f"Created user: {user.email}")

    # Create a turf
    turf = Turf.create(session, name='Green Turf', city='Nairobi', base_price_per_hour=50.0, latitude=-1.2864, longitude=36.8172)
    print(f"Created turf: {turf.name}")

    # Create a slot
    slot = TurfSlot.create(session, turf_id=turf.id, slot_date=date.today(), start_time='10:00', end_time='11:00', final_price=50.0)
    print(f"Created slot: {slot.start_time} - {slot.end_time}")

    # Create a booking
    booking = Booking.create(session, turf_id=turf.id, slot_id=slot.id, user_id=user.id, booking_date=date.today(), total_amount=50.0)
    print(f"Created booking: {booking.id}")

    # Read operations
    user_from_db = User.get_by_id(session, user.id)
    print(f"Retrieved user: {user_from_db.email}")

    turfs_in_city = Turf.get_by_city(session, 'Nairobi')
    print(f"Turfs in Nairobi: {len(turfs_in_city)}")

    # Update user
    user.update(session, city='Mombasa')
    print(f"Updated user city: {user.city}")

    # Association methods
    user_bookings = user.get_bookings(session)
    print(f"User bookings: {len(user_bookings)}")

    available_slots = turf.get_available_slots(session)
    print(f"Available slots for turf: {len(available_slots)}")

    # Aggregate methods
    total_user_bookings = user.get_total_bookings(session)
    print(f"Total user bookings: {total_user_bookings}")

    total_turf_revenue = turf.get_total_revenue(session)
    print(f"Total turf revenue: {total_turf_revenue}")

    # Delete booking
    booking.delete(session)
    print("Deleted booking")

    # Check remaining bookings
    remaining_bookings = Booking.get_all(session)
    print(f"Remaining bookings: {len(remaining_bookings)}")

    session.close()

if __name__ == '__main__':
    main()