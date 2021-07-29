import datetime
from functools import partial

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router

app = FastAPI(
    title="Tafelberg Rentals API",
    description="""This is a CORS-enabled API that scrapes the Rockport Escapes website for availability and pricing of the **Tafelberg** rental properties: Muizenberg, Sea Point, Simon's Town, and Pier Heaven.""",
    version="1.0.0"
)

app.add_middleware(CORSMiddleware, allow_origins="*")

app.include_router(router)
