from pydantic import BaseModel

class AdminBase(BaseModel):
    username: str
    email: str
    password: str

class AdminCreate(AdminBase):
    pass

class Admin(AdminBase):
    id: int
    class Config:
        orm_mode = True