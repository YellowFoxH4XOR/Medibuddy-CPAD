"""
    Main Class which created Api object
"""
from fastapi import FastAPI
from routers import user, medicine, order
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Medibuddy", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(medicine.router)
app.include_router(order.router)