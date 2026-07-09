from pydantic import BaseModel

class PaymentCreate(BaseModel):
    customer_id: int
    payment_amount: float
    meals_purchased: int
    payment_type: str
    notes: str

class PaymentUpdate(BaseModel):
    customer_id: int
    payment_amount: float
    meals_purchased: int
    payment_type: str
    notes: str

class PaymentSummary(BaseModel):
    total_paid: float
    total_meals: int

class PaymentResponse(BaseModel):
    id: int
    customer_id: int
    payment_amount: float
    meals_purchased: int
    payment_type: str
    notes: str

    class Config:
        from_attributes = True