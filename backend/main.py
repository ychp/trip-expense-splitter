from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api import accounts, categories, transactions, statistics


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="家庭账本API",
    description="家庭财务管理系统后端API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts.router, prefix="/api/accounts", tags=["账户"])
app.include_router(categories.router, prefix="/api/categories", tags=["分类"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["流水"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["统计"])


@app.get("/")
async def root():
    return {"message": "家庭账本API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
