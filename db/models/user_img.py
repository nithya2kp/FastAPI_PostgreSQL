
from sqlalchemy import Column, Integer, LargeBinary, ForeignKey,String
from sqlalchemy.orm import relationship
from db.base_class import Base


# SQLAlchemy model for the Profile_Picture table
class Profile_Picture(Base):
    __tablename__ = "profilepicture"
    profile_picture = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)
    users = relationship("Users", back_populates="profile_picture")
    profile_id = Column(Integer, primary_key=True, index=True)
    file_ext = Column(String, nullable=False)