from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GenAI Marketing API",
    description="API for GenAI Marketing Webapp",
    version="1.0.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to GenAI Marketing API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
