from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from schemas.payment import PaymentCreate, PaymentResponse, PaymentUpdate, PaymentSummary
from typing import List
from database import get_db
from api.auth import get_current_user

router = APIRouter(
    prefix='/payments',
    tags = ["Payment details"]
)

@router.post("/", response_model = PaymentResponse)
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    try:
        new_payment = models.Payment(
            customer_id = payment.customer_id,
            payment_amount = payment.payment_amount,
            meals_purchased = payment.meals_purchased,
            payment_type = payment.payment_type,
            notes = payment.notes)

        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)

        return new_payment
    
    except Exception as e:
        db.rollback()
        print(e)  # or use logging
        raise HTTPException(
            status_code=500,
            detail="Failed to register payment"
    )
    
@router.get("/", response_model = List[PaymentResponse])
def get_all_payments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    all_payments = db.query(models.Payment).all()

    return all_payments

@router.get("/customer/{id}", response_model = List[PaymentResponse])
def get_payments_of_customers(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    payments = (
        db.query(models.Payment)
        .filter(models.Payment.customer_id == id)
        .all()
    )

    if not payments:
        raise HTTPException(
            status_code=404,
            detail="No payments found for this customer"
        )

    return payments

@router.get("/{id}", response_model = PaymentResponse)
def get_payment_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)): 
    payment_detail = (
        db.query(models.Payment)
        .filter(models.Payment.id == id)
        .first()
    )

    if payment_detail is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment_detail

@router.put("/{id}", response_model = PaymentResponse)
def update_payment_by_id(
    id: int,
    payment: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)): 
    payment_detail = (
        db.query(models.Payment)
        .filter(models.Payment.id == id)
        .first()
    )

    if payment_detail is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )
    
    payment_detail.customer_id = payment.customer_id
    payment_detail.payment_amount = payment.payment_amount
    payment_detail.meals_purchased = payment.meals_purchased
    payment_detail.payment_type = payment.payment_type
    payment_detail.notes = payment.notes

    db.commit()
    db.refresh(payment_detail)

    return payment_detail

@router.get("/customer/{id}/summary", response_model = PaymentSummary)
def get_payments_of_customer(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):

    payments = (
        db.query(models.Payment)
        .filter(models.Payment.customer_id == id)
        .all()
    )

    if not payments:
        raise HTTPException(
            status_code=404,
            detail="No payments found for this customer"
        )

    total_paid = 0
    total_meals = 0

    for payment in payments:
        total_paid += payment.payment_amount
        total_meals += payment.meals_purchased

    return {
        "total_paid": total_paid,
        "total_meals": total_meals
    }