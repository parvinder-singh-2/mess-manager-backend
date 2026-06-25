from pydantic import BaseModel

class CustomerCreate(BaseModel):
    customer_name: str
    phone_number: str
    address: str
    notes: str

class CustomerUpdate(BaseModel):
    customer_name: str
    phone_number: str
    address: str
    notes: str
    is_active: bool

class CustomerResponse(BaseModel):
    id: int
    customer_name: str
    phone_number: str
    address: str
    is_active: bool
    notes: str

    class Config:
        from_attributes = True