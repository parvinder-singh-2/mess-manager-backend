from pydantic import BaseModel
from typing import List


# ---------- Stats ----------

class DashboardStats(BaseModel):
    totalCustomers: int
    mealsServedToday: int
    todayRevenue: float
    pendingDeliveries: int
    outstandingBalance: float


# ---------- Revenue Chart ----------

class RevenuePoint(BaseModel):
    label: str
    amount: float


class RevenueChart(BaseModel):
    period: str
    data: List[RevenuePoint]


# ---------- Meal Distribution ----------

class MealDistributionItem(BaseModel):
    name: str
    value: int


# ---------- Payment Methods ----------

class PaymentMethodItem(BaseModel):
    name: str
    value: float


# ---------- Today's Deliveries ----------

class DashboardDelivery(BaseModel):
    id: int
    customerId: int
    customer: str
    address: str
    meal: str
    status: str


# ---------- Recent Payments ----------

class DashboardPayment(BaseModel):
    id: int
    customerId: int
    customer: str
    amount: float
    method: str
    time: str


# ---------- Charts ----------

class DashboardCharts(BaseModel):
    revenue: RevenueChart
    mealDistribution: List[MealDistributionItem]
    paymentMethods: List[PaymentMethodItem]


# ---------- Tables ----------

class DashboardTables(BaseModel):
    todayDeliveries: List[DashboardDelivery]
    recentPayments: List[DashboardPayment]


# ---------- Final Response ----------

class DashboardResponse(BaseModel):
    stats: DashboardStats
    charts: DashboardCharts
    tables: DashboardTables