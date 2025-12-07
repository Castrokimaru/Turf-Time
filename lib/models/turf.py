import uuid
from sqlalchemy import Column, String, Text, Float, Integer
from sqlalchemy.orm import validates
from . import Base, session

class Turf(Base):
    __tablename__ = 'turfs'

    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    base_price_per_hour = Column(Float, nullable=False)
    is_active = Column(Integer, default=1)

    @validates('name')
    def validate_name(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name cannot be empty and must be a string")
        return value

    @validates('city')
    def validate_city(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("City cannot be empty and must be a string")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        if value is not None and not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if value is not None and not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number")
        return value

    @validates('base_price_per_hour')
    def validate_base_price_per_hour(self, key, value):
        if value is None or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Base price per hour must be a non-negative number")
        return value

    @validates('is_active')
    def validate_is_active(self, key, value):
        if value not in [0, 1]:
            raise ValueError("Is active must be 0 or 1")
        return value

    def __repr__(self):
        return f'<Turf {self.id}: {self.name}, {self.city}, ${self.base_price_per_hour}/hr>'

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter_by(name=name).first()

    @classmethod
    def create(cls, session, name, city, latitude=None, longitude=None, base_price_per_hour=None, is_active=1):
        turf = cls(id=str(uuid.uuid4()), name=name, city=city, latitude=latitude, longitude=longitude, base_price_per_hour=base_price_per_hour, is_active=is_active)
        session.add(turf)
        session.commit()
        return turf

    def update(self, session):
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()
