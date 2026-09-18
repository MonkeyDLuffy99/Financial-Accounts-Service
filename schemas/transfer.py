from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from models.transfer import TransferStatus


class TransferRequest(BaseModel):
    source_account_id: str
    destination_account_id: str
    amount: Decimal = Field(..., gt=0)

    @model_validator(mode="after")
    def accounts_must_differ(self) -> "TransferRequest":
        if self.source_account_id == self.destination_account_id:
            raise ValueError("source_account_id and destination_account_id must differ")
        return self


class TransferResponse(BaseModel):
    id: str
    source_account_id: str
    destination_account_id: str
    amount: Decimal
    status: TransferStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)