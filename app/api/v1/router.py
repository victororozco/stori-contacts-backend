from fastapi import APIRouter
from app.api.v1 import contacts

api_router = APIRouter()
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])