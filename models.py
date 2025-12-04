from sqlalchemy import Column, Integer, String, Float, Date, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import uuid
from datetime import date

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    role = Column(Text, nullable=False, default='player')
    city = Column(Text)

    # Relationships
    bookings = relationship('Booking', back_populates='user')

    @classmethod
    def create(cls, session, email, password_hash, role='player', city=None):
        user = cls(email=email, password_hash=password_hash, role=role, city=city)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def get_by_id(cls, session, user_id):
        return session.query(cls).filter_by(id=user_id).first()

    @classmethod
    def get_by_email(cls, session, email):
        return session.query(cls).filter_by(email=email).first()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    # Association method
    def get_bookings(self, session):
        return session.query(Booking).filter_by(user_id=self.id).all()

    # Aggregate method
    def get_total_bookings(self, session):
        return session.query(Booking).filter_by(user_id=self.id).count()

class Turf(Base):
    __tablename__ = 'turfs'

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    base_price_per_hour = Column(Float, nullable=False)
    is_active = Column(Integer, default=1)

    # Relationships
    slots = relationship('TurfSlot', back_populates='turf')
    bookings = relationship('Booking', back_populates='turf')

    @classmethod
    def create(cls, session, name, city, base_price_per_hour, latitude=None, longitude=None, is_active=1):
        turf = cls(name=name, city=city, latitude=latitude, longitude=longitude, base_price_per_hour=base_price_per_hour, is_active=is_active)
        session.add(turf)
        session.commit()
        return turf

    @classmethod
    def get_by_id(cls, session, turf_id):
        return session.query(cls).filter_by(id=turf_id).first()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def get_by_city(cls, session, city):
        return session.query(cls).filter_by(city=city).all()

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    # Association method
    def get_slots(self, session):
        return session.query(TurfSlot).filter_by(turf_id=self.id).all()

    def get_available_slots(self, session, slot_date=None):
        query = session.query(TurfSlot).filter_by(turf_id=self.id, status='available')
        if slot_date:
            query = query.filter_by(slot_date=slot_date)
        return query.all()

    # Aggregate method
    def get_total_bookings(self, session):
        return session.query(Booking).filter_by(turf_id=self.id).count()

    def get_total_revenue(self, session):
        result = session.query(Booking.total_amount).filter_by(turf_id=self.id).all()
        return sum(amount for (amount,) in result)

class TurfSlot(Base):
    __tablename__ = 'turf_slots'

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    turf_id = Column(Text, ForeignKey('turfs.id'), nullable=False)
    slot_date = Column(Date, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    status = Column(Text, default='available')
    final_price = Column(Float, nullable=False)

    # Relationships
    turf = relationship('Turf', back_populates='slots')
    bookings = relationship('Booking', back_populates='slot')

    @classmethod
    def create(cls, session, turf_id, slot_date, start_time, end_time, final_price, status='available'):
        slot = cls(turf_id=turf_id, slot_date=slot_date, start_time=start_time, end_time=end_time, status=status, final_price=final_price)
        session.add(slot)
        session.commit()
        return slot

    @classmethod
    def get_by_id(cls, session, slot_id):
        return session.query(cls).filter_by(id=slot_id).first()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    # Association method
    def get_booking(self, session):
        return session.query(Booking).filter_by(slot_id=self.id).first()

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    turf_id = Column(Text, ForeignKey('turfs.id'), nullable=False)
    slot_id = Column(Text, ForeignKey('turf_slots.id'), nullable=False)
    user_id = Column(Text, ForeignKey('users.id'), nullable=False)
    booking_date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Text, default='pending')

    # Relationships
    turf = relationship('Turf', back_populates='bookings')
    slot = relationship('TurfSlot', back_populates='bookings')
    user = relationship('User', back_populates='bookings')

    @classmethod
    def create(cls, session, turf_id, slot_id, user_id, booking_date, total_amount, status='pending'):
        booking = cls(turf_id=turf_id, slot_id=slot_id, user_id=user_id, booking_date=booking_date, total_amount=total_amount, status=status)
        session.add(booking)
        session.commit()
        return booking

    @classmethod
    def get_by_id(cls, session, booking_id):
        return session.query(cls).filter_by(id=booking_id).first()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    # Association method
    def get_user(self, session):
        return session.query(User).filter_by(id=self.user_id).first()

    def get_turf(self, session):
        return session.query(Turf).filter_by(id=self.turf_id).first()

    def get_slot(self, session):
        return session.query(TurfSlot).filter_by(id=self.slot_id).first()

# Database setup
engine = create_engine('sqlite:///turf_time.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)