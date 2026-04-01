# Quick Start Guide

## Prerequisites Check
```bash
python3 --version   # Need 3.8+
node --version      # Need 18+
ls secrets.env      # Should exist
ls sc_token.json    # Should exist (run python3 SC_Token.py if missing)
```

## Start Application

**Terminal 1 - Backend:**
```bash
./start_backend.sh
```
Wait for: "Uvicorn running on http://127.0.0.1:8000"

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh
```
Wait for: "Local: http://localhost:5173/"

**Browser:**
```
http://localhost:5173
```

## First Run

1. Check green dot in header (authenticated)
2. Leave default 168 hours (7 days)
3. Click "Start Run"
4. Wait for status: RUNNING → COMPLETED
5. View songs and albums in tables
6. Scroll down to see history graph

## Troubleshooting

**Backend won't start?**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend won't start?**
```bash
cd frontend
npm install
```

**Token expired?**
```bash
python3 SC_Token.py
```

**Reset database?**
```bash
rm data/app.db
# Restart backend
```

## API Endpoints

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/health
- Auth Status: http://localhost:8000/api/auth/status

## Stop Application

Press `Ctrl+C` in both terminals

## Next Steps

See detailed guides:
- `GETTING_STARTED.md` - Full setup instructions
- `README_WEB_APP.md` - Architecture and features
- `PROJECT_SUMMARY.md` - Implementation details
