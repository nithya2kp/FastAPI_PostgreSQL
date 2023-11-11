from sqlalchemy.orm import Session
from  fastapi import HTTPException
from sqlalchemy import insert,select,update, delete
from schemas.users import UserCreate,UserUpdate
from db.models.users import Users
from core.hashing import Hasher
from db.models.user_img import Profile_Picture

# Function to get user by user_id from db
def get_user_by_id(db: Session, id= int):
    return db.query(Users).filter(Users.user_id == id).first()

# Function to create new user in db
def create_new_user(user:UserCreate,db:Session):
    user=Users(
        full_name = user.full_name,
        email =user.email,
        password = user.password,
        phone =user.phone
    )
    db.add(user)       #  add user
    db.commit()        # save changes in db
    db.refresh(user)   # refresh details
    return user


# Function to update user details in db
def update_user(db: Session, user_id: str, full_name: str = None, password: str = None, phone: str = None, email: str = None):
    # Construct the update statement
    update_stmt = update(Users).where(Users.user_id == user_id)

    # Update the specified fields
    if full_name is not None:
        update_stmt = update_stmt.values(full_name=full_name)
    if password is not None:
        update_stmt = update_stmt.values(password=password)
    if phone is not None:
        update_stmt = update_stmt.values(phone=phone)
    if email is not None:
        update_stmt = update_stmt.values(email=email)
    # Execute the update statement
    result = db.execute(update_stmt)

    # Commit the changes
    db.commit()

    # Check if any rows were affected
    if result.rowcount > 0:
        return {"message": "User updated successfully"}
    else:
        return {"message": "User not found"}

# Function to delete user from db
def delete_user(db: Session, user_id: int):
    delete_stmt = delete(Profile_Picture).where(Profile_Picture.user_id == user_id)
    db.execute(delete_stmt)
    delete_user_smt= delete(Users).where(Users.user_id == user_id)
    result = db.execute(delete_user_smt)
    db.commit()
    # Check if any rows were affected
    if result.rowcount > 0:
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not found"}
