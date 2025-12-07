import uuid
from sqlalchemy import Column, String, Text, Float, Date, Integer, ForeignKey
from sqlalchemy.orm import validates, relationship
from . import Base, session
from .turf_slot import TurfSlot

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Text, primary_key=True)
    turf_id = Column(Text, ForeignKey('turfs.id'), nullable=False)
    slot_id = Column(Text, ForeignKey('turf_slots.id'), nullable=False)
    user_id = Column(Text, ForeignKey('users.id'), nullable=False)
    booking_date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Text, default='pending')

    turf = relationship('Turf', backref='bookings')
    slot = relationship('TurfSlot', backref='bookings')
    user = relationship('User', backref='bookings')

    @validates('turf_id')
    def validate_turf_id(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("Turf ID cannot be empty and must be a string")
        return value

    @validates('slot_id')
    def validate_slot_id(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("Slot ID cannot be empty and must be a string")
        return value

    @validates('user_id')
    def validate_user_id(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("User ID cannot be empty and must be a string")
        return value

    @validates('booking_date')
    def validate_booking_date(self, key, value):
        if not value:
            raise ValueError("Booking date cannot be empty")
        return value

    @validates('total_amount')
    def validate_total_amount(self, key, value):
        if value is None or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Total amount must be a non-negative number")
        return value

    @validates('status')
    def validate_status(self, key, value):
        if value not in ['pending', 'confirmed', 'cancelled']:
            raise ValueError("Status must be 'pending', 'confirmed', or 'cancelled'")
        return value

    def __repr__(self):
        return f'<Booking {self.id}: Turf {self.turf_id}, Slot {self.slot_id}, User {self.user_id}, {self.booking_date}, ${self.total_amount}, {self.status}>'

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def create(cls, session, turf_id, slot_id, user_id, booking_date, total_amount, status='pending'):
        # Check if slot is available
        slot = session.query(TurfSlot).filter_by(id=slot_id).first()
        if not slot or slot.status != 'available':
            raise ValueError("Slot is not available")
        booking = cls(id=str(uuid.uuid4()), turf_id=turf_id, slot_id=slot_id, user_id=user_id, booking_date=booking_date, total_amount=total_amount, status=status)
        slot.status = 'booked'
        session.add(booking)
        session.commit()
        return booking

    def update(self, session):
        session.commit()

    def delete(self, session):
        # Set slot back to available if booking is deleted
        slot = session.query(TurfSlot).filter_by(id=self.slot_id).first()
        if slot:
            slot.status = 'available'
        session.delete(self)
        session.commit()
