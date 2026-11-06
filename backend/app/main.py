from datetime import datetime, timezone
from decimal import Decimal
from itertools import count
from threading import Lock

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Imperial Bank Demo API",
    version="0.2.0",
    description="Simulated banking API. No real funds or bank connections.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fictional data only. Storage resets when the API process restarts.
lock = Lock()
accounts = {
    "4829": {
        "id": "4829",
        "owner": "Aarav Sharma",
        "type": "savings",
        "balance": Decimal("845250.00"),
        "currency": "INR",
    },
    "9012": {
        "id": "9012",
        "owner": "Aarav Sharma",
        "type": "current",
        "balance": Decimal("120000.00"),
        "currency": "INR",
    },
}
beneficiaries = {
    "Meera Patel": {"account_id": "2176", "balance": Decimal("25000.00")},
    "Rohan Desai": {"account_id": "7301", "balance": Decimal("18000.00")},
}
transactions = [
    {
        "id": "TXN-1005",
        "account_id": "4829",
        "description": "Salary credited",
        "amount": "65000.00",
        "direction": "credit",
        "status": "completed",
        "created_at": "2026-11-06T09:00:00+05:30",
    }
]
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
    with lock:
        return [
            {**account, "balance": str(account["balance"])}
            for account in accounts.values()
        ]


@app.get("/api/beneficiaries")
def list_beneficiaries():
    return [
        {"name": name, "account_id": details["account_id"]}
        for name, details in beneficiaries.items()
    ]


@app.get("/api/transactions")
def list_transactions():
    with lock:
        return list(reversed(transactions))


@app.post("/api/transfers")
def create_transfer(payload: TransferRequest):
    with lock:
        source = accounts.get(payload.from_account)
        if not source:
            raise HTTPException(status_code=404, detail="Demo source account not found")

        destination = beneficiaries.get(payload.beneficiary)
        if not destination:
            raise HTTPException(status_code=404, detail="Choose a saved demo beneficiary")

        if payload.beneficiary == source["owner"]:
            raise HTTPException(status_code=400, detail="You cannot transfer to your own name")

        if source["balance"] < payload.amount:
            raise HTTPException(status_code=409, detail="Insufficient demo balance")

        source["balance"] -= payload.amount
        destination["balance"] += payload.amount
        created_at = datetime.now(timezone.utc).isoformat()
        transfer_id = next(ids)
        amount = str(payload.amount)

        debit = {
            "id": f"TXN-{transfer_id}",
            "account_id": payload.from_account,
            "description": f"Transfer to {payload.beneficiary}",
            "amount": amount,
            "direction": "debit",
            "status": "completed",
            "note": payload.note,
            "created_at": created_at,
        }
        credit = {
            "id": f"TXN-{transfer_id}-C",
            "account_id": destination["account_id"],
            "description": f"Transfer from {source['owner']}",
            "amount": amount,
            "direction": "credit",
            "status": "completed",
            "note": payload.note,
            "created_at": created_at,
        }
        transactions.extend([debit, credit])

        return {
            "message": "Demo transfer completed",
            "transaction": debit,
            "new_balance": str(source["balance"]),
        }
