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




