from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import router
from src.api.auth import router as auth_router
from src.api.scheduler import router as scheduler_router
from src.config.settings import Settings
from src.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Linked Post Generator",
    description="An AI-powered tool for generating linked social media posts",
    version="1.0.0"
)

# Load settings
settings = Settings()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(scheduler_router, prefix="/api/v1/scheduler", tags=["scheduler"])

# Start the scheduler
from src.api.scheduler import scheduler
scheduler.start()

@app.get("/")
async def root():
    return {"message": "Welcome to Linked Post Generator API"} 