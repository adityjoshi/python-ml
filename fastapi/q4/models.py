from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base



class Lot:
    __tablename__ = "lots"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    name = Column(String)
    zone = Column(String)
    slips = relationship("Slip",back_populates="lots",cascade="all, delete-orphan")

class Slip:
    __tablename__ = "slips"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    ticket_code = Column(String)
    vehicle_class = Column(String)
    parked_minute = Column(Integer)
    lot_id = Column(Integer,ForeignKey("lots.id"),nullable=False)
    lots = relationship("Lot",back_populates="slips")
