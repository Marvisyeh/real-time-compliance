from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from api.core.config import APIConfig
from api.core.logging import logger
from api.modules.events.router import router as events_router
from api.modules.dashboard.router import router as dashboard_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """application lifecycle management"""
    # start
    logger.info("API service starting...")
    yield
    # stop
    logger.info("API service stopping...")


app = FastAPI(
    title=APIConfig.API_TITLE,
    version=APIConfig.API_VERSION,
    description=APIConfig.API_DESCRIPTION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# register routes
app.include_router(events_router)
app.include_router(dashboard_router)


@app.get("/health")
def health_check():
    """health check endpoint"""
    return {
        "status": "ok",
        "service": APIConfig.API_TITLE,
        "version": APIConfig.API_VERSION
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """global exception handling"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if APIConfig.DEBUG else "Please contact the administrator"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=APIConfig.DEBUG
    )
