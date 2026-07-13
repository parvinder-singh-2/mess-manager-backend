from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class DeliveryStatus(str, Enum):
    pending = "Pending"
    delivered = "Delivered"


class DeliveryItem(BaseModel):
    delivery_id: int
    customer_id: int
    customer_name: str
    phone: str
    address: str
    meal: str
    quantity: int
    service: str
    delivery_time: datetime | None = None
    notes: str | None = None
    status: DeliveryStatus


class DeliveryStats(BaseModel):
    today_deliveries: int
    pending: int
    delivered: int
    remaining: int
    completion_percentage: int


class DeliverySummary(BaseModel):
    total: int
    delivered: int
    pending: int


class DeliveryDashboardResponse(BaseModel):
    stats: DeliveryStats
    deliveries: list[DeliveryItem]
    summary: DeliverySummary


class DeliveryUpdateRequest(BaseModel):
    delivery_id: int
    status: DeliveryStatus
    delivery_time: datetime | None = None
    notes: str | None = None


class DeliveryUpdateResponse(BaseModel):
    message: str
    delivery: DeliveryItem