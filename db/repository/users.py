from sqlalchemy.orm import Session
from  fastapi import HTTPException
from schemas.users import UserCreate,UserUpdate
from db.models.users import Users
from core.hashing import Hasher

# Function to get user by user_id from db
def get_user_by_id(db: Session, id= int):
    return db.query(Users).filter(Users.user_id == id).first()

# Function to create new user in db
def create_new_user(user:UserCreate,db:Session):
    user=Users(
        full_name = user.full_name,
        email =user.email,
        password = Hasher.get_password_hash(user.password),
        phone =user.phone
    )
    db.add(user)       #  add user
    db.commit()        # save changes in db
    db.refresh(user)   # refresh details
    return user


# Function to update user details in db
def update_user(db: Session,user_id:int,full_name:str,email: str,password: str,phone:str):
    user = get_user_by_id(db=db,user_id=user_id)
    user.full_name=full_name
    user.email=email
    user.password=password
    user.phone=phone
    db.commit()
    db.refresh(user)
    return user

# Function to delete user from db
def delete_user(db:Session,user_id:int):
    user = get_user_by_id(db=db,user_id=user_id)
    db.delete(user)
    db.commit()

