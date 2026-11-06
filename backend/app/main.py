from datetime import datetime, timezone
from decimal import Decimal
from itertools import count
from threading import Lock
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Imperial Bank Demo API", version="0.1.0", description="Simulated banking API. No real funds or bank connections.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Fictional seed data. Replace in-memory storage with PostgreSQL + SQLAlchemy in the persistence phase.
lock = Lock()
accounts = {"4829": {"id": "4829", "owner": "Aarav Sharma", "type": "savings", "balance": Decimal("845250.00"), "currency": "INR"}, "9012": {"id": "9012", "owner": "Aarav Sharma", "type": "current", "balance": Decimal("120000.00"), "currency": "INR"}}
transactions = [{"id": "TXN-1005", "account_id": "4829", "description": "Salary credited", "amount": "65000.00", "direction": "credit", "status": "completed", "created_at": "2026-11-06T09:00:00+05:30"}]
ids = count(1006)

class TransferRequest(BaseModel):
    from_account: str = Field(default="4829", min_length=4, max_length=4)
    beneficiary: str = Field(min_length=2, max_length=80)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    note: str = Field(default="", max_length=120)

@app.get("/health")
def health():
    return {"status": "ok", "mode": "demo", "real_banking": False}

@app.get("/api/accounts")
def list_accounts():
    return [{**a, "balance": str(a["balance"])} for a in accounts.values()]

@app.get("/api/transactions")
def list_transactions():
    return list(reversed(transactions))

@app.post("/api/transfers")
def create_transfer(payload: TransferRequest):
    with lock:
        account = accounts.get(payload.from_account)
        if not account:
            raise HTTPException(status_code=404, detail="Demo account not found")
        if account["balance"] < payload.amount:
            raise HTTPException(status_code=409, detail="Insufficient demo balance")
        account["balance"] -= payload.amount
        txn = {"id": f"TXN-{next(ids)}", "account_id": payload.from_account, "description": f"Transfer to {payload.beneficiary}", "amount": str(payload.amount), "direction": "debit", "status": "completed", "note": payload.note, "created_at": datetime.now(timezone.utc).isoformat()}
        transactions.append(txn)
        return {"message": "Demo transfer completed", "transaction": txn, "new_balance": str(account["balance"])}
