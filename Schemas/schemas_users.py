from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class AddUpdateUserSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True
