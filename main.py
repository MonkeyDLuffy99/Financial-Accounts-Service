from fastapi import FastAPI

from models import account, transaction, transfer  # noqa: F401 - registers tables on Base
from database import Base, engine
from routers.accounts import router as accounts_router
from routers.transfers import router as transfers_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Accounts & Transfers Microservice")

app.include_router(accounts_router)
app.include_router(transfers_router)