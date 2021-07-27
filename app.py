from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import property_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*"
)

app.include_router(
    property_router,
    prefix="/properties"
)

