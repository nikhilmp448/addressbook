from sqlalchemy import Column, Integer, String
from database import Base

class Address(Base):
    """
    Create an Address model with fields
    """
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    coordinates = Column(String)
    address = Column(String)
    