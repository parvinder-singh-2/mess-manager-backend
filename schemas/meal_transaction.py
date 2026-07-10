from pydantic import BaseModel
from datetime import datetime

class MealTransactionCreate(BaseModel):
    customer_id: int
    meal_type: str
    quantity: int
    meal_rate: float
    total_amount: float
    service_type: str
    is_delivered: bool


class MealTransactionUpdate(BaseModel):
    customer_id: int
    meal_type: str
    quantity: int
    meal_rate: float
    total_amount: float
    service_type: str
    is_delivered: bool


class MealTransactionResponse(BaseModel):
    id: int
    customer_id: int
    meal_type: str
    quantity: int
    meal_rate: float
    total_amount: float
    service_type: str
    is_delivered: bool
    created_at: datetime

    class Config:
        from_attributes = True