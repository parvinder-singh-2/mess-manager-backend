from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

import models

from database import get_db
from api.auth import get_current_user

from schemas.deliveries import (
    DeliveryDashboardResponse,
    DeliveryItem,
    DeliveryStats,
    DeliverySummary,
    DeliveryUpdateRequest,
    DeliveryUpdateResponse,
    DeliveryStatus,
)

router = APIRouter(
    prefix="/deliveries",
    tags=["Delivery"]
)

@router.get("/dashboard", response_model=DeliveryDashboardResponse)
def get_delivery_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    today = date.today()

    records = (
        db.query(models.MealTransaction, models.Customer)
        .join(
            models.Customer,
            models.MealTransaction.customer_id == models.Customer.id
        )
        .filter(
            func.date(models.MealTransaction.created_at) == today
        )
        .all()
    )

    deliveries = []

    delivered = 0

    for meal, customer in records:

        status = (
            DeliveryStatus.delivered
            if meal.is_delivered
            else DeliveryStatus.pending
        )

        if meal.is_delivered:
            delivered += 1

        deliveries.append(
            DeliveryItem(
                delivery_id=meal.id,
                customer_id=customer.id,
                customer_name=customer.customer_name,
                phone=customer.phone_number,
                address=customer.address,
                meal=meal.meal_type,
                quantity=meal.quantity,
                service=meal.service_type,
                delivery_time=meal.created_at,
                notes=customer.notes,
                status=status,
            )
        )

    total = len(deliveries)
    pending = total - delivered

    completion = (
        int((delivered / total) * 100)
        if total > 0
        else 0
    )

    return DeliveryDashboardResponse(
        stats=DeliveryStats(
            today_deliveries=total,
            pending=pending,
            delivered=delivered,
            remaining=pending,
            completion_percentage=completion,
        ),
        deliveries=deliveries,
        summary=DeliverySummary(
            total=total,
            delivered=delivered,
            pending=pending,
        ),
    )


@router.put("/{id}", response_model=DeliveryUpdateResponse)
def update_delivery(
    id: int,
    request: DeliveryUpdateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    meal = (
        db.query(models.MealTransaction)
        .filter(models.MealTransaction.id == id)
        .first()
    )

    if not meal:
        raise HTTPException(
            status_code=404,
            detail="Delivery not found"
        )

    meal.is_delivered = (
        request.status == DeliveryStatus.delivered
    )

    db.commit()
    db.refresh(meal)

    customer = (
        db.query(models.Customer)
        .filter(models.Customer.id == meal.customer_id)
        .first()
    )

    return DeliveryUpdateResponse(
        message="Delivery updated successfully",
        delivery=DeliveryItem(
            delivery_id=meal.id,
            customer_id=customer.id,
            customer_name=customer.customer_name,
            phone=customer.phone_number,
            address=customer.address,
            meal=meal.meal_type,
            quantity=meal.quantity,
            service=meal.service_type,
            delivery_time=meal.created_at,
            notes=customer.notes,
            status=(
                DeliveryStatus.delivered
                if meal.is_delivered
                else DeliveryStatus.pending
            ),
        ),
    )