import logging
from typing import Annotated
from fastapi import FastAPI, HTTPException, Request, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import api_router


logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Image Object Detection Service")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info("Received request: %s %s", request.method, request.url)
    response = await call_next(request)
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "Internal server error"})


@app.get("/")
async def home_status():
    return {"status": "alive"}


app.include_router(prefix='/api', router=api_router)
