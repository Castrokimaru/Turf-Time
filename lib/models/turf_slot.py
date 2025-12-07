import uuid
from sqlalchemy import Column, String, Text, Float, Date, Integer, ForeignKey
from sqlalchemy.orm import validates, relationship
from . import Base, session

class TurfSlot(Base):
    __tablename__ = 'turf_slots'

    id = Column(Text, primary_key=True)
    turf_id = Column(Text, ForeignKey('turfs.id'), nullable=False)
    slot_date = Column(Date, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    status = Column(Text, default='available')
    final_price = Column(Float, nullable=False)

    turf = relationship('Turf', backref='slots')

    @validates('turf_id')
    def validate_turf_id(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("Turf ID cannot be empty and must be a string")
        return value

    @validates('slot_date')
    def validate_slot_date(self, key, value):
        if not value:
            raise ValueError("Slot date cannot be empty")
        return value

    @validates('start_time')
    def validate_start_time(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("Start time cannot be empty and must be a string")
        return value

    @validates('end_time')
    def validate_end_time(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("End time cannot be empty and must be a string")
        return value

    @validates('status')
    def validate_status(self, key, value):
        if value not in ['available', 'booked', 'cancelled']:
            raise ValueError("Status must be 'available', 'booked', or 'cancelled'")
        return value

    @validates('final_price')
    def validate_final_price(self, key, value):
        if value is None or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Final price must be a non-negative number")
        return value

    def __repr__(self):
        return f'<TurfSlot {self.id}: Turf {self.turf_id}, {self.slot_date} {self.start_time}-{self.end_time}, {self.status}, ${self.final_price}>'

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def find_by_turf_id(cls, session, turf_id):
        return session.query(cls).filter_by(turf_id=turf_id).all()

    @classmethod
    def create(cls, session, turf_id, slot_date, start_time, end_time, final_price, status='available'):
        slot = cls(id=str(uuid.uuid4()), turf_id=turf_id, slot_date=slot_date, start_time=start_time, end_time=end_time, status=status, final_price=final_price)
        session.add(slot)
        session.commit()
        return slot

    def update(self, session):
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()
