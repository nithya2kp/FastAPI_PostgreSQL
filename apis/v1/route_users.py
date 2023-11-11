from fastapi import  APIRouter,Depends,HTTPException,status,File,UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from schemas.users import UserCreate,UserUpdate,Response,RequestNew
from db.session import get_db
from db.models import user_img
from db.repository.users import create_new_user,update_user,delete_user,get_user_by_id

router=APIRouter()     #instance of APIRouter


# route for new user create
@router.post("/")
def create_user( user : UserCreate,db:Session=Depends(get_db)):
    user =create_new_user(user = user,db=db)
    return user

# route for get user  details using user_id
@router.get("/{user_id}")
def get_by_id(user_id:int,db:Session=Depends(get_db)):
    user = get_user_by_id(db,user_id)
    return  Response(code=200,status="ok",message="Success get data",result=user).dict(exclude_none=True)

# Endpoint get image: postgre db
@router.get('/image/{user_id}')
async def view(user_id : int, db: Session = Depends(get_db)):
        images_query = db.query(models.user_img.Profile_Picture.profile_picture,models.user_img.Profile_Picture.file_ext).filter(
        models.user_img.Profile_Picture.user_id == user_id).first()
        if images_query:
            img_path = f"images/{images_query[0]}{images_query[1]}"
            return FileResponse(img_path)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


# Endpoint upload image: postgre sql
@router.post("/upload/{user_id}")
async def upload_image(user_id: int,file : UploadFile = File(...),   db: Session = Depends(get_db)):
    img_ext = ['.jpg', '.jpeg', '.png', '.gif','.webp','.tif', '.psd', '.heif', '.heic', '.svg']
    image_data = os.path.splitext(file.filename)

    images_query = db.query(models.user_img.Profile_Picture).filter(
    models.user_img.Profile_Picture.profile_picture == image_data[0],models.user_img.Profile_Picture.file_ext==image_data[1],
    models.user_img.Profile_Picture.user_id == user_id ).first()


    if not images_query:
        data = {"profile_picture": image_data[0], "user_id": user_id, "file_ext": image_data[1]}
        add_query = models.user_img.Profile_Picture(**data)
        db.add(add_query)
        db.commit()
        db.refresh(add_query)
        file.filename = image_data
        contents = await file.read()

        with open(IMAGEDIR+str(image_data[0])+str(image_data[1]), "wb") as f:
            f.write(contents)

        return {"filename": file.filename}
    else:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail="This image already exists for the user")

    return {"image_data": add_query}


@router.delete("/delete")
def delete_user_details(user_id: int, db: Session = Depends(get_db)):
    result = delete_user(db, user_id=user_id)
    return Response(code=200, status="ok", message=result["message"], result=None).dict(exclude_none=True)


@router.post("/update")
def update_user_details(request: RequestNew,db:Session = Depends(get_db)):
    _user = update_user(db,user_id=request.parameter.user_id,full_name=request.parameter.full_name,password=request.parameter.password,phone=request.parameter.phone,email=request.parameter.email)
    return Response(code=200,status="ok",message="Success update data",result=_user)
