from fastapi import  APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from schemas.users import UserCreate,UserUpdate,Response,RequestNew
from db.session import get_db
from db.repository.users import create_new_user,update_user,delete_user,get_user_by_id

router=APIRouter()     #instance of APIRouter


# route for new user create
@router.post("/")
def create_user( user : UserCreate,db:Session=Depends(get_db)):
    user =create_new_user(user = user,db=db)
    return user

# route for update details
@router.post("/update")
def update_user_details(request: RequestNew,db:Session = Depends(get_db)):
    _user = update_user(db,user_id=request.parameter.user_id,full_name=request.parameter.full_name,password=request.parameter.password,phone=request.parameter.phone,email=request.parameter.email)
    return Response(code=200,status="ok",message="Success update data",result=_user)

# route for delete details
@router.delete("/{user_id}")
def delete_user_details(user_id: int, db: Session = Depends(get_db)):
    delete_user(db,user_id=user_id)
    return Response(code=200,status="ok",message="Success deletion User",result=user).dict(exclude_none=True)

# route for get user  details using user_id
@router.get("/{user_id}")
def get_by_id(user_id:int,db:Session=Depends(get_db)):
    user = get_user_by_id(db,user_id)
    return  Response(code=200,status="ok",message="Success get data",result=user).dict(exclude_none=True)