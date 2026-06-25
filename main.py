from fastapi import FastAPI
import models
from database import engine
from api.customers import router as customer_router
from api.payments import router as payment_router
from api.meal_transactions import router as meal_router
from api.auth import router as auth_router

app = FastAPI()

app.include_router(customer_router)
app.include_router(payment_router)
app.include_router(meal_router)
app.include_router(auth_router)

@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)

# db_dependency = Annotated[Session, Depends(get_db)]

