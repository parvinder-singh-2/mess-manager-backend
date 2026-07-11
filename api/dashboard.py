from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from schemas.dashboard import DashboardResponse

# Import your models
from models import Customer
from models import Payment
from models import MealTransaction
from models import CustomerAccount
import traceback

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):

    try:
            # EVERYTHING currently inside get_dashboard()
        today = date.today()

        # ==========================================================
        # Stats
        # ==========================================================

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

        # ==========================================================
        # Revenue Chart (Last 7 Days)
        # ==========================================================

        revenue_chart = []

        for i in range(6, -1, -1):
            day = today - timedelta(days=i)

            amount = (
                db.query(func.coalesce(func.sum(Payment.amount), 0))
                .filter(func.date(Payment.created_at) == day)
                .scalar()
            )

            revenue_chart.append(
                {
                    "label": day.strftime("%a"),
                    "amount": amount,
                }
            )

        # ==========================================================
        # Meal Distribution
        # ==========================================================

        meal_distribution_query = (
            db.query(
                MealTransaction.service_type,
                func.count(MealTransaction.id),
            )
            .group_by(MealTransaction.service_type)
            .all()
        )

        meal_distribution = [
            {
                "name": meal,
                "value": count,
            }
            for meal, count in meal_distribution_query
        ]

        # ==========================================================
        # Payment Methods
        # ==========================================================

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
                "name": method,
                "value": amount,
            }
            for method, amount in payment_methods_query
        ]

        # ==========================================================
        # Today's Deliveries
        # ==========================================================

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
                "meal": delivery.service_type,
                "status": (
                    "Delivered"
                    if delivery.is_delivered
                    else "Pending"
                ),
            }
            for delivery in deliveries
        ]

        # ==========================================================
        # Recent Payments
        # ==========================================================

        payments = (
            db.query(Payment)
            .join(Customer)
            .order_by(Payment.created_at.desc())
            .limit(10)
            .all()
        )

        recent_payments = [
            {
                "id": payment.id,
                "customerId": payment.customer.id,
                "customer": payment.customer.name,
                "amount": payment.payment_amount,
                "method": payment.payment_type,
                "time": payment.payment_datetime.strftime("%I:%M %p"),
            }
            for payment in payments
        ]

        # ==========================================================
        # Final Response
        # ==========================================================

        return {
            "stats": {
                "totalCustomers": total_customers,
                "mealsServedToday": meals_served_today,
                "todayRevenue": today_revenue,
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


    except Exception as e:
        traceback.print_exc()
        raise e