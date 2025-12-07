from models import Session, Base, engine
from models.user import User
from models.turf import Turf
from models.turf_slot import TurfSlot
from models.booking import Booking
from datetime import date

def seed_database():
    # Drop tables if they exist
    Base.metadata.drop_all(engine)
    # Create tables
    Base.metadata.create_all(engine)

    session = Session()
    try:
        # Seed users
        user1 = User.create(session, 'player1@example.com', 'hashedpass1', 'player', 'New York')
        user2 = User.create(session, 'admin@example.com', 'hashedpass2', 'admin', 'Los Angeles')

        # Seed turfs
        turf1 = Turf.create(session, 'Central Park Turf', 'New York', 40.7829, -73.9654, 50.0, 1)
        turf2 = Turf.create(session, 'Hollywood Turf', 'Los Angeles', 34.0928, -118.3287, 60.0, 1)

        # Seed turf slots
        slot1 = TurfSlot.create(session, turf1.id, date(2023, 10, 1), '10:00', '11:00', 50.0)
        slot2 = TurfSlot.create(session, turf1.id, date(2023, 10, 1), '11:00', '12:00', 50.0)
        slot3 = TurfSlot.create(session, turf2.id, date(2023, 10, 2), '14:00', '15:00', 60.0)

        # Seed bookings
        booking1 = Booking.create(session, turf1.id, slot1.id, user1.id, date(2023, 9, 30), 50.0)

        print("Database seeded successfully!")
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
