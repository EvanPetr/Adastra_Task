from pydantic import BaseModel, EmailStr


class Profile(BaseModel):
    name: str
    email: EmailStr
