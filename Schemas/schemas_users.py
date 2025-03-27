from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True


class UpdateUserSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True
