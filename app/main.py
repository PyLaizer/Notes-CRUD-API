from fastapi import FastAPI
from app.routers import notes
from app.db import init_db

app = FastAPI()

app.include_router(notes.router)

# Database Initializer
init_db()