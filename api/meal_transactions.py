from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from schemas.meal_transaction import MealTransactionCreate, MealTransactionResponse, MealTransactionUpdate
from typing import List
from database import get_db
from sqlalchemy import func
from api.auth import get_current_user


router = APIRouter(
    prefix='/meal-transactions',
    tags = ["Meal Transaction details"]
)

@router.post("/", response_model=MealTransactionResponse)
def create_meal_transaction(
    meal_transaction: MealTransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        new_transaction = models.MealTransaction(
            customer_id=meal_transaction.customer_id,
            meal_type=meal_transaction.meal_type,
            quantity=meal_transaction.quantity,
            meal_rate=meal_transaction.meal_rate,
            total_amount=meal_transaction.total_amount,
            service_type=meal_transaction.service_type,
            is_delivered=meal_transaction.is_delivered,
        )

        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        return new_transaction

    except Exception as e:
        db.rollback()
        print(repr(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/", response_model = List[MealTransactionResponse])
def get_all_meal_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    all_meals_transactions = db.query(models.MealTransaction).all()

    return all_meals_transactions

@router.get("/{id}", response_model = MealTransactionResponse)
def get_meal_transaction_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):

    meal_transaction = db.query(models.MealTransaction)\
                        .filter(models.MealTransaction.id == id)\
                        .first()
    
    if not meal_transaction:
        raise HTTPException(
            status_code = 404,
            detail = "No Meals Found"
        )
    
    return meal_transaction

@router.put("/{id}", response_model = MealTransactionResponse)
def update_meal_transaction(
    id: int,
    meal_transaction: MealTransactionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):

    existing_transaction = (
        db.query(models.MealTransaction)
        .filter(models.MealTransaction.id == id)
        .first()
    )

    if not existing_transaction:
        raise HTTPException(
            status_code = 404,
            detail = "No Meals Found"
        )
    
    existing_transaction.customer_id = meal_transaction.customer_id
    existing_transaction.meal_type = meal_transaction.meal_type
    existing_transaction.quantity = meal_transaction.quantity
    existing_transaction.meal_rate = meal_transaction.meal_rate
    existing_transaction.total_amount = meal_transaction.total_amount
    existing_transaction.service_type = meal_transaction.service_type
    existing_transaction.is_delivered = meal_transaction.is_delivered
    db.commit()
    db.refresh(existing_transaction)

    return existing_transaction

@router.delete('/{id}')
def delete_meal_transaction(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):

    meal_transaction = (
        db.query(models.MealTransaction)
        .filter(models.MealTransaction.id == id)
        .first()
    )

    if not meal_transaction:
        raise HTTPException(
            status_code = 404,
            detail = "No Meals Found"
        )

    db.delete(meal_transaction)
    db.commit()

    return {"message": "Meal transaction deleted successfully"}

@router.get("/customer/{id}", response_model = List[MealTransactionResponse])
def get_meal_transactions_for_customer(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):

    meal_transactions = db.query(models.MealTransaction)\
                        .filter(models.MealTransaction.customer_id == id)\
                        .all()
    
    if not meal_transactions:
        raise HTTPException(
            status_code = 404,
            detail = "No Meals Found"
        )
    
    return meal_transactions

@router.get("/date/{date}", response_model = List[MealTransactionResponse])
def get_meal_transaction_for_date(
    date: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    meal_transactions = (
        db.query(models.MealTransaction)
        .filter(func.date(models.MealTransaction.created_at) == date)
        .all()
    )

    if not meal_transactions:
        raise HTTPException(
            status_code = 404,
            detail = "No Meals Found"
        )

    return meal_transactions

@router.get("/delivery/{date}", response_model = List[MealTransactionResponse])
def get_delivery_meal_transaction_for_date(
    date: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    meal_transactions = (
        db.query(models.MealTransaction)
        .filter(func.date(models.MealTransaction.created_at) == date)
        .filter(models.MealTransaction.service_type == "DELIVERY")
        .all()
    )

    if not meal_transactions:
        raise HTTPException(
            status_code = 404,
            detail = "No Meals Found"
        )

    return meal_transactions

@router.patch("/{id}/mark-delivered")
def mark_order_delivered(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    
    meal_transaction = (
        db.query(models.MealTransaction)
        .filter(models.MealTransaction.id == id)
        .first()
    )

    if not meal_transaction:
        raise HTTPException(
            status_code = 404,
            detail = "No Meals Found"
        )
    
    meal_transaction.is_delivered = True

    db.commit()
    db.refresh(meal_transaction)

    return {"message": "Order marked delivered"}