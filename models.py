from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, Numeric, DateTime, Enum
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, index = True)
    username = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    role = Column(Enum("ADMIN", "STAFF", name = "user_roles"), nullable = False)
    email = Column(String, unique = True, nullable = False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key= True, index = True)
    customer_name = Column(String, nullable = False)
    phone_number = Column(String, unique = True, nullable = False)
    address = Column(String, nullable = True)
    is_active = Column(Boolean, nullable = False, default = True)
    notes = Column(String, nullable = True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    #Relationships
    account = relationship("CustomerAccount", back_populates="customer", uselist=False)
    payments = relationship("Payment",back_populates="customer")
    meal_transactions = relationship("MealTransaction", back_populates="customer")

class CustomerAccount(Base):
    __tablename__ = "customer_accounts"

    id = Column(Integer, primary_key= True, index = True)
    customer_id = Column(Integer, ForeignKey("customers.id"), unique = True, nullable = False)
    meal_balance = Column(Integer, nullable = False, default = 0)
    empty_tiffins = Column(Integer, nullable = False, default = 0)
    lunch_quantity = Column(Integer, nullable = False, default = 0)
    dinner_quantity = Column(Integer, nullable = False, default = 0)
    service_type = Column(Enum("DELIVERY", "DINEIN", 'TAKEOUT', name = 'service_type'), nullable = False, default = "DELIVERY")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    #Relationships
    customer = relationship("Customer", back_populates="account")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key = True, index = True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable = False)
    payment_amount = Column(Numeric(10, 2), nullable = False)
    meals_purchased = Column(Integer, nullable = False)
    payment_type = Column(Enum("CASH", "ONLINE", name = "payment_method"), nullable = False)
    payment_datetime = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    notes = Column(String, nullable = True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    #Relationships
    customer = relationship("Customer", back_populates="payments")

class MealTransaction(Base):
    __tablename__ = "meal_transactions"

    id = Column(Integer, primary_key = True, index = True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable = False)
    meal_type = Column(Enum("LUNCH", "DINNER", name = "meal_type"), nullable = False)
    quantity = Column(Integer, nullable = False)
    total_amount = Column(Numeric(10, 2), nullable = False)
    service_type = Column(Enum("DELIVERY", "DINEIN", 'TAKEOUT', name = 'service_type'), nullable = False)
    is_delivered = Column(Boolean, default = False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    #Relationships
    customer = relationship("Customer", back_populates="meal_transactions")

