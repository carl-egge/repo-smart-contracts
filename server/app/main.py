import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Slowapi is a library to add rate limiting to your FastAPI application.
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from app.config import get_config
from app.db import db
from app.rest import contracts

# create the app
app = FastAPI(title="Repository Smart Contracts")


# add rate limiting
limiter = Limiter(key_func=get_remote_address, headers_enabled=True, default_limits=["1000/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


# add cors
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# create base router
app.include_router(contracts.router, prefix='/api', tags=["Contracts"],)


@app.on_event("startup")
async def startup():
    config = get_config()
    await db.connect_to_database(path=config.db_path)


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
