from pydantic import BaseModel
from typing import Optional, List


class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    is_active: Optional[bool]
    is_admin: Optional[bool]

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    user: int

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class OrderItemsSchema(BaseModel):
    quantity: int
    flavor: str
    size: str
    price: float

    class Config:
        from_attributes = True


class ResponseOrderSchema(BaseModel):
    id: int
    status: str
    price: float
    items: List[OrderItemsSchema]

    class Config:
        from_attributes = True
