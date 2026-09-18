# Running the Financial Accounts & Transfers Microservice

## 1. Prerequisites

- Python **3.12** or **3.13** is required (some packages fail to install on 3.14)
- `pip` available on your PATH

To check which version of python runs:
```bash
python --version
```

## 2. Set up a virtual environment

From the app directory run:

**Windows (PowerShell):**
```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` appear at the start of your terminal prompt once activated.

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the service

```bash
uvicorn main:app --reload
```

The service runs on:
```
http://127.0.0.1:8000
```

The database file (`financial_accounts.db`) is created automatically on service startup.

## 5. Explore the API interactively

FastAPI generates interactive docs automatically. While the server is running you can open:

- **Swagger UI:** http://127.0.0.1:8000/docs

## 6. Stop the service

To stop the service press `Ctrl + C`

## Quick end-to-end test sequence

```bash
# 1. Create two accounts
curl -X POST http://127.0.0.1:8000/accounts -H "Content-Type: application/json" \
  -d '{"owner_name":"Alice","opening_balance":"100.00"}'

curl -X POST http://127.0.0.1:8000/accounts -H "Content-Type: application/json" \
  -d '{"owner_name":"Bob","opening_balance":"0.00"}'

# 2. Copy the "id" from each response, then transfer between them
curl -X POST http://127.0.0.1:8000/transfers -H "Content-Type: application/json" \
  -d '{"source_account_id":"<ALICE_ID>","destination_account_id":"<BOB_ID>","amount":"30.00"}'

# 3. Confirm balances and ledger updated
curl http://127.0.0.1:8000/accounts/<ALICE_ID>
curl http://127.0.0.1:8000/accounts/<ALICE_ID>/transactions
```