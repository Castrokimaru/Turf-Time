import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import validates
from . import Base, session

class User(Base):
    __tablename__ = 'users'

    id = Column(Text, primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    role = Column(Text, nullable=False, default='player')
    city = Column(Text)

    @validates('email')
    def validate_email(self, key, value):
        if not value or not isinstance(value, str) or '@' not in value:
            raise ValueError("Email cannot be empty and must be a valid email address")
        return value

    @validates('password_hash')
    def validate_password_hash(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("Password hash cannot be empty and must be a string")
        return value

    @validates('role')
    def validate_role(self, key, value):
        if value not in ['player', 'admin']:
            raise ValueError("Role must be 'player' or 'admin'")
        return value

    @validates('city')
    def validate_city(self, key, value):
        if value and not isinstance(value, str):
            raise ValueError("City must be a string")
        return value

    def __repr__(self):
        return f'<User {self.id}: {self.email}, {self.role}, {self.city}>'

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, session, email):
        return session.query(cls).filter_by(email=email).first()

    @classmethod
    def create(cls, session, email, password_hash, role='player', city=None):
        user = cls(id=str(uuid.uuid4()), email=email, password_hash=password_hash, role=role, city=city)
        session.add(user)
        session.commit()
        return user

    def update(self, session):
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()
