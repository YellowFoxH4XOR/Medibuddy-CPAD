"""
    Main Class which created Api object
"""
from fastapi import FastAPI
from routers import user, medicine, order

app = FastAPI(title="Medibuddy", version="1.0.0")

app.include_router(user.router)
app.include_router(medicine.router)
app.include_router(order.router)