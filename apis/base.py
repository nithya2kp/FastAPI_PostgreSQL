from  fastapi import APIRouter
from apis.v1 import  route_users

api_router = APIRouter()   # Create an instance of APIRoute
api_router.include_router(route_users.router,prefix="",tags=["users"])   # Include the user routes from the route_users