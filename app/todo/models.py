from sqlalchemy import  Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Todo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True, index=True)
    mission = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('User.id'),index=True)
    user = relationship("User", back_populates="todos")