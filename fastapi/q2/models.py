from sqlalchemy import String,Integer,Column,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    name = Column(String)
    city = Column(String)
    items = relationship("Item",back_populates="stores",cascade="all,delete-orphan")

Class Item(Base):
    __tablename__ = "items"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    name = Column(String)
    category = Column(String)
    stock_qty = Column(Integer)
    store_id = Column(Integer,ForeignKey("stores.id"),nullable=False)
    stores = relationship("Store",back_populates="items")


