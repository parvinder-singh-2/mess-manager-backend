from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from schemas.customer_account import CustomerAccountResponse, CustomerAccountUpdate
from api.auth import get_current_user
from typing import List

from database import get_db

router = APIRouter(
    prefix='/customers',
    tags = ["Customer details"]
)


@router.post("/", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    existing_customer = (
        db.query(models.Customer)
        .filter(
            models.Customer.phone_number == customer.phone_number
        )
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail="Customer already exists"
        )

    try:
        new_customer = models.Customer(
            customer_name=customer.customer_name.lower().strip(),
            phone_number=customer.phone_number.strip(),
            address=customer.address.lower().strip(),
            notes=customer.notes
        )

        db.add(new_customer)
        db.flush()  # Generates ID without committing

        new_account = models.CustomerAccount(
            customer_id=new_customer.id
        )

        db.add(new_account)

        db.commit()
        db.refresh(new_customer)

        return new_customer

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create customer"
        )

@router.get("/", response_model= List[CustomerResponse])
def get_all_customers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    
    all_customers = db.query(models.Customer).all()

    return all_customers

@router.get("/search", response_model=CustomerResponse)
def get_customer(
    current_user: models.User = Depends(get_current_user),
    name: str | None = None,
    phone_number: str | None = None,
    address: str | None = None,
    id: int | None = None,
    db: Session = Depends(get_db)):
    if id is not None:
        customer = (
            db.query(models.Customer)
            .filter(models.Customer.id == id)
            .first()
        )

    elif phone_number:
        customer = (
            db.query(models.Customer)
            .filter(models.Customer.phone_number == phone_number.strip())
            .first()
        )

    elif name:
        customer = (
            db.query(models.Customer)
            .filter(models.Customer.customer_name == name.strip().lower())
            .first()
        )

    elif address:
        customer = (
            db.query(models.Customer)
            .filter(models.Customer.address == address.strip().lower())
            .first()
        )

    else:
        raise HTTPException(
            status_code=400,
            detail="Provide a search parameter"
        )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer

@router.put("/{id}", response_model=CustomerResponse)
def update_customer(
    id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):

    # Check if customer exists
    existing_customer = (
        db.query(models.Customer)
        .filter(models.Customer.id == id)
        .first()
    )

    if not existing_customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Update fields
    existing_customer.customer_name = (
        customer.customer_name.lower().strip()
    )

    existing_customer.phone_number = (
        customer.phone_number.strip()
    )

    existing_customer.address = (
        customer.address.lower().strip()
    )

    existing_customer.notes = customer.notes

    duplicate_customer = (
                            db.query(models.Customer)
                            .filter(
                            models.Customer.phone_number == customer.phone_number.strip(),
                            models.Customer.id != id)
                            .first()
)

    if duplicate_customer:
        raise HTTPException(
        status_code=400,
        detail="Phone number already exists"
    )

    db.commit()
    db.refresh(existing_customer)

    return existing_customer

@router.patch("/{id}/deactivate")
def deactivate_customer(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    customer = db.query(models.Customer)\
                 .filter(models.Customer.id == id)\
                 .first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.is_active = False
    db.commit()

    return {"message": "Customer deactivated"}

@router.patch("/{id}/reactivate")
def reactivate_customer(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    customer = db.query(models.Customer)\
                 .filter(models.Customer.id == id)\
                 .first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.is_active = True
    db.commit()

    return {"message": "Customer reactivated"}

@router.get("/{id}/account", response_model = CustomerAccountResponse)
def get_customer_account(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    
    customer_account = db.query(models.CustomerAccount)\
                        .filter(models.CustomerAccount.customer_id == id)\
                        .first()
    
    if not customer_account:
        raise HTTPException(
        status_code=404,
        detail="Customer account not found"
    )
    
    return customer_account

@router.put("/{id}/account", response_model = CustomerAccountResponse)
def update_customer_account(
    id: int,
    account: CustomerAccountUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):

    # Check if customer exists
    existing_customer = (
        db.query(models.CustomerAccount)
        .filter(models.CustomerAccount.customer_id == id)
        .first()
    )

    if not existing_customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Update fields
    existing_customer.meal_balance = account.meal_balance
    existing_customer.empty_boxes_pending = account.empty_boxes_pending
    existing_customer.lunch_quantity = account.lunch_quantity
    existing_customer.dinner_quantity = account.dinner_quantity
    existing_customer.service_type = account.service_type
    existing_customer.is_paused = account.is_paused

    db.commit()
    db.refresh(existing_customer)

    return existing_customer

@router.delete('/{id}')
def delete_customer(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):

    customer = (
            db.query(models.Customer)
            .filter(models.Customer.id == id)
            .first()
        )

    if not customer:
        raise HTTPException(
            status_code = 404,
            detail = "No Customer Found"
        )

    db.delete(customer)
    db.commit()

    return {"message": "Customer deleted successfully"}