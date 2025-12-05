# Database models for Turf-Time application
# Uses SQLAlchemy ORM for database operations

from sqlalchemy import create_engine, Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, validates
import uuid

# Set up SQLAlchemy base and engine
Base = declarative_base()
engine = create_engine('sqlite:///turf_time.db')
Session = sessionmaker(bind=engine)

class User(Base):
    # User model representing application users
    # Has one-to-many relationship with Bookings
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default='player')
    city = Column(String)

    bookings = relationship('Booking', back_populates='user')

    @validates('email')
    def validate_email(self, key, value):
        if not value or '@' not in value:
            raise ValueError("Invalid email address")
        return value

    @validates('password_hash')
    def validate_password_hash(self, key, value):
        if not value:
            raise ValueError("Password hash cannot be empty")
        return value

    @validates('role')
    def validate_role(self, key, value):
        if value not in ['player', 'admin']:
            raise ValueError("Role must be 'player' or 'admin'")
        return value

    @classmethod
    def create(cls, session, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    def delete(cls, session, id):
        obj = session.query(cls).filter_by(id=id).first()
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, session, email):
        return session.query(cls).filter_by(email=email).first()

class Turf(Base):
    __tablename__ = 'turfs'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    base_price_per_hour = Column(Float, nullable=False)
    is_active = Column(Integer, default=1)

    slots = relationship('TurfSlot', back_populates='turf')
    bookings = relationship('Booking', back_populates='turf')

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Name cannot be empty")
        return value

    @validates('city')
    def validate_city(self, key, value):
        if not value:
            raise ValueError("City cannot be empty")
        return value

    @validates('base_price_per_hour')
    def validate_base_price_per_hour(self, key, value):
        if value <= 0:
            raise ValueError("Base price per hour must be positive")
        return value

    @validates('is_active')
    def validate_is_active(self, key, value):
        if value not in [0, 1]:
            raise ValueError("Is active must be 0 or 1")
        return value

    # ORM methods for database operations
    @classmethod
    def create(cls, session, **kwargs):
        # Create a new user instance and save to database
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    def delete(cls, session, id):
        # Delete user by ID, return True if successful
        obj = session.query(cls).filter_by(id=id).first()
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        # Retrieve all users from database
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        # Find user by ID
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter_by(name=name).all()

class TurfSlot(Base):
    __tablename__ = 'turf_slots'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    turf_id = Column(String, ForeignKey('turfs.id'), nullable=False)
    slot_date = Column(Date, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    status = Column(String, default='available')
    final_price = Column(Float, nullable=False)

    turf = relationship('Turf', back_populates='slots')
    bookings = relationship('Booking', back_populates='slot')

    @validates('start_time')
    def validate_start_time(self, key, value):
        # Simple validation, assume HH:MM format
        if not value or len(value) != 5 or value[2] != ':':
            raise ValueError("Start time must be in HH:MM format")
        return value

    @validates('end_time')
    def validate_end_time(self, key, value):
        if not value or len(value) != 5 or value[2] != ':':
            raise ValueError("End time must be in HH:MM format")
        return value

    @validates('status')
    def validate_status(self, key, value):
        if value not in ['available', 'booked', 'cancelled']:
            raise ValueError("Status must be 'available', 'booked', or 'cancelled'")
        return value

    @validates('final_price')
    def validate_final_price(self, key, value):
        if value < 0:
            raise ValueError("Final price cannot be negative")
        return value

    @classmethod
    def create(cls, session, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    def delete(cls, session, id):
        obj = session.query(cls).filter_by(id=id).first()
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def find_by_turf_id(cls, session, turf_id):
        return session.query(cls).filter_by(turf_id=turf_id).all()

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    turf_id = Column(String, ForeignKey('turfs.id'), nullable=False)
    slot_id = Column(String, ForeignKey('turf_slots.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    booking_date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default='pending')

    turf = relationship('Turf', back_populates='bookings')
    slot = relationship('TurfSlot', back_populates='bookings')
    user = relationship('User', back_populates='bookings')

    @validates('total_amount')
    def validate_total_amount(self, key, value):
        if value < 0:
            raise ValueError("Total amount cannot be negative")
        return value

    @validates('status')
    def validate_status(self, key, value):
        if value not in ['pending', 'confirmed', 'cancelled']:
            raise ValueError("Status must be 'pending', 'confirmed', or 'cancelled'")
        return value

    @classmethod
    def create(cls, session, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    def delete(cls, session, id):
        obj = session.query(cls).filter_by(id=id).first()
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def find_by_user_id(cls, session, user_id):
        return session.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def find_by_turf_id(cls, session, turf_id):
        return session.query(cls).filter_by(turf_id=turf_id).all()

# Create tables
Base.metadata.create_all(engine)