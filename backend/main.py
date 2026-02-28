from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api import categories, transactions, trips, members, wallets, stats, wallet_flows, reconciliation

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(log_dir=settings.DATA_DIR)
    logger.info("Application starting up...")
    yield
    logger.info("Application shutting down...")


app = FastAPI(
    title="出行账本API",
    description="旅行费用分摊管理系统",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router, prefix="/api/categories", tags=["分类"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["交易记录"])
app.include_router(trips.router, prefix="/api/trips", tags=["行程"])
app.include_router(members.router, prefix="/api/members", tags=["成员"])
app.include_router(wallets.router, prefix="/api/wallets", tags=["钱包"])
app.include_router(stats.router, prefix="/api/stats", tags=["统计分析"])
app.include_router(wallet_flows.router, prefix="/api/wallet-flows", tags=["余额流水"])
app.include_router(reconciliation.router, prefix="/api/reconciliation", tags=["结算建议"])


@app.get("/")
async def root():
    return {"message": "出行账本API", "version": "1.0.0", "features": ["行程管理", "费用分摊", "智能结算"]}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
