from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.account import Account
from database import get_db
from models.transaction import Transaction, TransactionType
from models.transfer import Transfer, TransferStatus
from schemas.transfer import TransferRequest, TransferResponse

router = APIRouter(prefix="/transfers", tags=["transfers"])


@router.post("", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
def create_transfer(payload: TransferRequest, db: Session = Depends(get_db)):
    source = db.get(Account, payload.source_account_id)
    if source is None:
        raise HTTPException(status_code=404, detail=f"Account '{payload.source_account_id}' not found")

    destination = db.get(Account, payload.destination_account_id)
    if destination is None:
        raise HTTPException(status_code=404, detail=f"Account '{payload.destination_account_id}' not found")

    if Decimal(source.balance) < payload.amount:
        raise HTTPException(status_code=409, detail="Insufficient funds")

    transfer = Transfer(
        source_account_id=source.id,
        destination_account_id=destination.id,
        amount=payload.amount,
        status=TransferStatus.COMPLETED,
    )
    db.add(transfer)
    db.flush()

    source.balance = Decimal(source.balance) - payload.amount
    destination.balance = Decimal(destination.balance) + payload.amount

    db.add(Transaction(
        account_id=source.id,
        type=TransactionType.DEBIT,
        amount=payload.amount,
        balance_after=source.balance,
        transfer_id=transfer.id,
    ))
    db.add(Transaction(
        account_id=destination.id,
        type=TransactionType.CREDIT,
        amount=payload.amount,
        balance_after=destination.balance,
        transfer_id=transfer.id,
    ))

    db.commit()
    db.refresh(transfer)
    return transfer