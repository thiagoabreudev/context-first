"""
Context-First Platform API

FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Context-First API",
    version="0.1.0",
    description="AI Development Governance & Orchestration Platform",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "context-first-api"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Context-First API",
        "version": "0.1.0",
        "docs": "/docs",
    }


# TODO: Add routers in IAD-8
# from interfaces.api.v1 import projects, demands, metaspecs
# app.include_router(projects.router, prefix="/v1")
# app.include_router(demands.router, prefix="/v1")
# app.include_router(metaspecs.router, prefix="/v1")
