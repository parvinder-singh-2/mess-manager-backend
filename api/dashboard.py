from fastapi import APIRouter
from schemas.dashboard import DashboardResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/", response_model=DashboardResponse)
def get_dashboard():

    return {
        "stats": {
            "totalCustomers": 128,
            "mealsServedToday": 356,
            "todayRevenue": 18560,
            "pendingDeliveries": 18,
            "outstandingBalance": 34250,
        },

        "charts": {

            "revenue": {
                "period": "week",
                "data": [
                    {"label": "Mon", "amount": 8200},
                    {"label": "Tue", "amount": 15200},
                    {"label": "Wed", "amount": 12100},
                    {"label": "Thu", "amount": 21000},
                    {"label": "Fri", "amount": 16100},
                    {"label": "Sat", "amount": 14100},
                    {"label": "Sun", "amount": 17800},
                ]
            },

            "mealDistribution": [
                {
                    "name": "Lunch",
                    "value": 1286
                },
                {
                    "name": "Dinner",
                    "value": 1091
                }
            ],

            "paymentMethods": [
                {
                    "name": "CASH",
                    "value": 18500
                },
                {
                    "name": "ONLINE",
                    "value": 42750
                }
            ]
        },

        "tables": {

            "todayDeliveries": [
                {
                    "id": 1,
                    "customerId": 5,
                    "customer": "Rahul Sharma",
                    "address": "Vijay Nagar",
                    "meal": "Lunch",
                    "status": "Delivered"
                },
                {
                    "id": 2,
                    "customerId": 7,
                    "customer": "Anjali Verma",
                    "address": "Scheme 54",
                    "meal": "Dinner",
                    "status": "Pending"
                }
            ],

            "recentPayments": [
                {
                    "id": 10,
                    "customerId": 5,
                    "customer": "Rahul Sharma",
                    "amount": 2500,
                    "method": "ONLINE",
                    "time": "5 min ago"
                },
                {
                    "id": 11,
                    "customerId": 7,
                    "customer": "Anjali Verma",
                    "amount": 1800,
                    "method": "CASH",
                    "time": "20 min ago"
                }
            ]
        }
    }