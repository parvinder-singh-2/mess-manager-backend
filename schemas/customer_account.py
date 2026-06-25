from pydantic import BaseModel

class CustomerAccountCreate(BaseModel):
    meal_balance: int
    empty_boxes_pending: int
    lunch_quantity: int
    dinner_quantity: int
    service_type: str
    is_paused: bool

class CustomerAccountUpdate(BaseModel):
    meal_balance: int
    empty_boxes_pending: int
    lunch_quantity: int
    dinner_quantity: int
    service_type: str
    is_paused: bool

class CustomerAccountResponse(BaseModel):
    meal_balance: int
    empty_boxes_pending: int
    lunch_quantity: int
    dinner_quantity: int
    service_type: str
    is_paused: bool

    class Config:
        from_attributes = True