from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from models.transaction import TransactionType


class AccountCreateRequest(BaseModel):
    owner_name: str = Field(..., min_length=1, max_length=255)
    opening_balance: Decimal = Field(default=Decimal("0.00"), ge=0)


class AccountResponse(BaseModel):
    id: str
    owner_name: str
    balance: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionResponse(BaseModel):
    id: str
    account_id: str
    type: TransactionType
    amount: Decimal
    balance_after: Decimal
    transfer_id: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)