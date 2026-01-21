"""
Main application file for the Full-Stack Web Todo Application.

This module sets up the FastAPI application with all routes and middleware.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.auth import router as auth_router
from .api.v1.tasks import router as tasks_router
from .config import settings


# Create the FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="REST API for the Full-Stack Web Todo Application",
    debug=settings.debug,
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routers
app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])
app.include_router(tasks_router, prefix="/api/v1", tags=["Tasks"])


@app.get("/")
def read_root():
    """
    Root endpoint for the API.

    Returns:
        dict: Welcome message and API information
    """
    return {
        "message": "Welcome to the Full-Stack Web Todo Application API",
        "version": settings.version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint for the API.

    Returns:
        dict: Health status
    """
    return {"status": "healthy", "timestamp": __import__('datetime').datetime.utcnow().isoformat()}


# For running the application directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"]
    )