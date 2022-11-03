"""
    Main Class which created Api object
"""

from unicodedata import name
from fastapi import Depends, FastAPI
from internal import token
from routers import user, tweet

app = FastAPI(title="Medibuddy", version="1.0.0")

app.include_router(user.router)