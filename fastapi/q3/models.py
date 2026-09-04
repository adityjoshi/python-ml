from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship
from database import Base



class Notebook(Base):
    __tablename__ = "notebooks"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    title = Column(String)
    author = Column(String)
    entries = relationship("Entry", back_populates="notebooks", cascade="all, delete-orphan")

class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    heading = Column(String)
    mood = Column(String)
    word_count = Column(Integer)
    notebook_id = Column(Integer,ForeignKey("notebooks.id"),nullable=False)
    notebooks = relationship("Notebook", back_populates="entries")

    
