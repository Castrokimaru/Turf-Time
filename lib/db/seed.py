# Database seeding script

from .models import Session, User, Turf, TurfSlot, Booking
import datetime

def seed_database():
    session = Session()
    try:
        # Check if already seeded
        existing_users = session.query(User).count()
        if existing_users > 0:
            print("Database already seeded. Skipping.")
            return

        # Create users
        user1 = User.create(session, email='player1@example.com', password_hash='hash1', role='player', city='Nairobi')
        user2 = User.create(session, email='admin@example.com', password_hash='hash2', role='admin', city='Mombasa')

        # Create turfs
        turf1 = Turf.create(session, name='Green Field', city='Nairobi', latitude=-1.2864, longitude=36.8172, base_price_per_hour=100.0, is_active=1)
        turf2 = Turf.create(session, name='Blue Pitch', city='Mombasa', latitude=-4.0435, longitude=39.6682, base_price_per_hour=120.0, is_active=1)

        # Create turf slots
        slot1 = TurfSlot.create(session, turf_id=turf1.id, slot_date=datetime.date(2023, 12, 10), start_time='10:00', end_time='11:00', status='available', final_price=100.0)
        slot2 = TurfSlot.create(session, turf_id=turf1.id, slot_date=datetime.date(2023, 12, 10), start_time='11:00', end_time='12:00', status='booked', final_price=100.0)
        slot3 = TurfSlot.create(session, turf_id=turf2.id, slot_date=datetime.date(2023, 12, 11), start_time='14:00', end_time='15:00', status='available', final_price=120.0)

        # Create bookings
        booking1 = Booking.create(session, turf_id=turf1.id, slot_id=slot2.id, user_id=user1.id, booking_date=datetime.date(2023, 12, 5), total_amount=100.0, status='confirmed')

        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == '__main__':
    seed_database()