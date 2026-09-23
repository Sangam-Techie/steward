"""Entry point for the Steward Control Plane FastAPI application.

Sets up the application instance, registers routers, and exposes
a health check endpoint.
"""

from fastapi import FastAPI

from app.routers.auth import router as auth_router

app = FastAPI(title="Steward Control Plane")
app.include_router(auth_router)


@app.get("/health")
async def health():
    """Return the service health status."""
    return {"status": "ok"}
