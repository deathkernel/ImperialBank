# Imperial Bank

A responsive, simulated banking web application built for learning and demonstration. **No real money, banking rails, or payment providers are connected.**

## Project structure

- `frontend/` — Next.js 15, React 19, TypeScript, Tailwind CSS and Recharts.
- `backend/` — FastAPI demo API with an in-memory simulation ledger.

## Requirements

- Node.js 20.9+
- Python 3.10+

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000.

## Run the backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is available at http://127.0.0.1:8000 and its OpenAPI docs at http://127.0.0.1:8000/docs.

## Connect the frontend to the API

The frontend API client defaults to `http://localhost:8000`. To use a different backend URL, create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Restart the Next.js development server after changing environment variables. Start both the FastAPI backend and Next.js frontend for live demo balances and transfers.

The demo API exposes:
- `GET /health` — demo service status.
- `GET /api/accounts` — fictional customer accounts.
- `GET /api/beneficiaries` — saved fictional beneficiaries.
- `GET /api/transactions` — demo ledger entries.
- `POST /api/transfers` — validates and simulates a transfer, recording matching debit and credit entries.

Transfers update the in-memory source and beneficiary balances. Data resets when the backend restarts; this is not a persistent or production ledger.

## Demo safety

All displayed account details and transactions are fictional. The backend currently uses in-memory demo data, which resets when the server restarts. It is not production banking software and must not be used to store real customer information or credentials.

## Roadmap

- Persist demo users, accounts and ledger entries in PostgreSQL.
- Add proper authentication and role-based authorization.
- Add atomic double-entry transfers and idempotency safeguards.
- Add tests, audit events and operational monitoring.
