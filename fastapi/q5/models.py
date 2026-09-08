from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Boutique(Base):
    __tablename__ = "boutiques"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    city = Column(String)

    products = relationship(
        "Product", back_populates="boutique", cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    category = Column(String)
    price = Column(Integer)
    highlighted = Column(Boolean, default=False)
    boutique_id = Column(Integer, ForeignKey("boutiques.id"), nullable=False)

    boutique = relationship("Boutique", back_populates="products")
