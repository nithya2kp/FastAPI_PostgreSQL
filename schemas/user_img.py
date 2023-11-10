from pydantic import BaseModel

class File(BaseModel):
        profile_picture: str
        user_id: int
        file_ext: str