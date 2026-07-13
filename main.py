from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine
from api.customers import router as customer_router
from api.payments import router as payment_router
from api.meal_transactions import router as meal_router
from api.auth import router as auth_router
from api.dashboard import router as dashboard_router
from api.deliveries import router as delivery_router

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:5173",  
    "https://mess-manager.vercel.app",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(customer_router)
app.include_router(payment_router)
app.include_router(meal_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(delivery_router)


@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)