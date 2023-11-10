from fastapi import FastAPI,File,UploadFile,HTTPException,Depends,status,Request
from core.config import settings
from db.base import  Base
from db.session import engine,get_db
from apis.base import route_users
import psycopg2
from sqlalchemy.orm import Session
import os
from db import models
from db.models import user_img
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates


# For storing images
IMAGEDIR = "images/"

def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    return app


app = start_application()
templates = Jinja2Templates(directory="templates")

# Endpoint Test "Hello Fast API"
@app.get("/")
async def home(request: Request):
        return templates.TemplateResponse("item.html",{"request": request, "msg":"Hello FastAPI🚀"})

app.include_router(route_users.router,prefix="",tags=["users"])

# db parameters postgresql
db_params = {
    "dbname": "python_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

# posgresql db connection
def create_connection():
    conn = psycopg2.connect(**db_params)
    curr = conn.cursor()
    return conn, curr

# Endpoint upload image: postgre sql
@app.post("/upload/{user_id}")
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

# Endpoint get image: postgre db
@app.get('/image/{user_id}')
async def view(user_id : int, db: Session = Depends(get_db)):
        images_query = db.query(models.user_img.Profile_Picture.profile_picture,models.user_img.Profile_Picture.file_ext).filter(
        models.user_img.Profile_Picture.user_id == user_id).first()
        if images_query:
            img_path = f"images/{images_query[0]}{images_query[1]}"
            return FileResponse(img_path)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

