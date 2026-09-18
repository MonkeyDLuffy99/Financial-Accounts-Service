from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.account import Account
from models.database import get_db
from models.transaction import Transaction
from schemas.account import AccountCreateRequest, AccountResponse, TransactionResponse

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(payload: AccountCreateRequest, db: Session = Depends(get_db)):
    account = Account(owner_name=payload.owner_name, balance=payload.opening_balance)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: str, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail=f"Account '{account_id}' not found")
    return account


@router.get("/{account_id}/transactions", response_model=list[TransactionResponse])
def list_transactions(account_id: str, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail=f"Account '{account_id}' not found")

    return (
        db.query(Transaction)
        .filter(Transaction.account_id == account_id)
        .order_by(Transaction.created_at.asc())
        .all()
    )