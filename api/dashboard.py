from datetime import date, timedelta
import traceback

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from schemas.dashboard import DashboardResponse

from models import (
    Customer,
    CustomerAccount,
    MealTransaction,
    Payment,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    try:

        today = date.today()

        # =====================================================
        # Stats
        # =====================================================

        total_customers = db.query(Customer).count()

        meals_served_today = (
            db.query(func.coalesce(func.sum(MealTransaction.quantity), 0))
            .filter(func.date(MealTransaction.created_at) == today)
            .scalar()
        )

        today_revenue = (
            db.query(func.coalesce(func.sum(Payment.payment_amount), 0))
            .filter(func.date(Payment.payment_datetime) == today)
            .scalar()
        )

        pending_deliveries = (
            db.query(MealTransaction)
            .filter(
                func.date(MealTransaction.created_at) == today,
                MealTransaction.service_type == "DELIVERY",
                MealTransaction.is_delivered == False,
            )
            .count()
        )

        outstanding_balance = (
            db.query(func.coalesce(func.sum(CustomerAccount.meal_balance), 0))
            .scalar()
        )

        # =====================================================
        # Revenue Chart
        # =====================================================

        revenue_chart = []

        for i in range(6, -1, -1):

            day = today - timedelta(days=i)

            amount = (
                db.query(func.coalesce(func.sum(Payment.payment_amount), 0))
                .filter(func.date(Payment.payment_datetime) == day)
                .scalar()
            )

            revenue_chart.append(
                {
                    "label": day.strftime("%a"),
                    "amount": float(amount or 0),
                }
            )

        # =====================================================
        # Meal Distribution
        # =====================================================

        meal_distribution_query = (
            db.query(
                MealTransaction.meal_type,
                func.sum(MealTransaction.quantity),
            )
            .group_by(MealTransaction.meal_type)
            .all()
        )

        meal_distribution = [
            {
                "name": meal,
                "value": qty,
            }
            for meal, qty in meal_distribution_query
        ]

        # =====================================================
        # Payment Methods
        # =====================================================

        payment_methods_query = (
            db.query(
                Payment.payment_type,
                func.sum(Payment.payment_amount),
            )
            .group_by(Payment.payment_type)
            .all()
        )

        payment_methods = [
            {
                "name": payment_type,
                "value": float(amount or 0),
            }
            for payment_type, amount in payment_methods_query
        ]

        # =====================================================
        # Today's Deliveries
        # =====================================================

        deliveries = (
            db.query(MealTransaction)
            .join(Customer)
            .filter(
                func.date(MealTransaction.created_at) == today,
                MealTransaction.service_type == "DELIVERY",
            )
            .limit(10)
            .all()
        )

        today_deliveries = [
            {
                "id": delivery.id,
                "customerId": delivery.customer.id,
                "customer": delivery.customer.customer_name,
                "address": delivery.customer.address,
                "meal": delivery.meal_type,
                "status": (
                    "Delivered"
                    if delivery.is_delivered
                    else "Pending"
                ),
            }
            for delivery in deliveries
        ]

        # =====================================================
        # Recent Payments
        # =====================================================

        payments = (
            db.query(Payment)
            .join(Customer)
            .order_by(Payment.payment_datetime.desc())
            .limit(10)
            .all()
        )

        recent_payments = [
            {
                "id": payment.id,
                "customerId": payment.customer.id,
                "customer": payment.customer.customer_name,
                "amount": float(payment.payment_amount),
                "method": payment.payment_type,
                "time": payment.payment_datetime.strftime("%I:%M %p"),
            }
            for payment in payments
        ]

        # =====================================================
        # Response
        # =====================================================

        return {
            "stats": {
                "totalCustomers": total_customers,
                "mealsServedToday": meals_served_today,
                "todayRevenue": float(today_revenue or 0),
                "pendingDeliveries": pending_deliveries,
                "outstandingBalance": outstanding_balance,
            },
            "charts": {
                "revenue": {
                    "period": "week",
                    "data": revenue_chart,
                },
                "mealDistribution": meal_distribution,
                "paymentMethods": payment_methods,
            },
            "tables": {
                "todayDeliveries": today_deliveries,
                "recentPayments": recent_payments,
            },
        }

    except Exception:
        traceback.print_exc()
        raise