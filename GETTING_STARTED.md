# Getting Started with SoundCloud Weekly Updater Web App

This guide will help you set up and run the web application for the first time.

## Prerequisites

Before starting, ensure you have:

1. **Python 3.8+** installed
   ```bash
   python3 --version
   ```

2. **Node.js 18+** and npm installed
   ```bash
   node --version
   npm --version
   ```

3. **SoundCloud OAuth credentials** in `secrets.env`:
   ```env
   SC_CLIENT_ID=your_client_id_here
   SC_CLIENT_SECRET=your_client_secret_here
   ```

4. **Valid OAuth token** in `sc_token.json`:
   - If you don't have this, run: `python3 SC_Token.py`
   - Follow the OAuth flow to generate your token

## Quick Start (Recommended)

### Option 1: Using Startup Scripts

**Terminal 1 - Backend:**
```bash
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh
```

The scripts will automatically:
- Create virtual environments
- Install dependencies
- Start both servers

### Option 2: Manual Setup

**Terminal 1 - Backend:**
```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

## Verify Installation

### Step 1: Check Backend

1. Open http://localhost:8000/docs
2. You should see the FastAPI Swagger documentation
3. Try the `/api/health` endpoint - should return `{"status": "ok"}`
4. Try the `/api/auth/status` endpoint - should show `authenticated: true`

### Step 2: Check Frontend

1. Open http://localhost:5173
2. You should see the SoundCloud Weekly Updater dashboard
3. Look for the green authentication indicator in the header
4. The form to create a new run should be visible

### Step 3: Test a Run

1. In the frontend, enter hours to look back (try 24 for testing)
2. Click "Start Run"
3. Watch the status change from "RUNNING" to "COMPLETED"
4. View the songs and albums found
5. Check that albums show "✓ Liked" status

## Troubleshooting

### Backend Issues

**Error: `ModuleNotFoundError: No module named 'fastapi'`**
- Solution: Activate venv and install dependencies
  ```bash
  cd backend
  source venv/bin/activate
  pip install -r requirements.txt
  ```

**Error: `FileNotFoundError: Token file not found`**
- Solution: Generate OAuth token
  ```bash
  python3 SC_Token.py
  ```

**Error: Token expired or authentication failed**
- Solution: The app should auto-refresh tokens, but if it fails:
  ```bash
  python3 SC_Token.py  # Regenerate token
  rm data/app.db       # Clear database (optional)
  ```

**Error: `ImportError: cannot import name 'SCClient'`**
- This is expected - our app reimplements SCClient
- Verify `backend/app/services/sc_client.py` exists

### Frontend Issues

**Error: `ECONNREFUSED` when making API calls**
- Solution: Ensure backend is running on port 8000
  ```bash
  curl http://localhost:8000/api/health
  ```

**Blank page or React errors**
- Solution: Clear node_modules and reinstall
  ```bash
  cd frontend
  rm -rf node_modules
  npm install
  npm run dev
  ```

**CORS errors in browser console**
- Solution: Verify CORS settings in `backend/app/main.py`
- Ensure frontend is on http://localhost:5173

### Script Execution Issues

**Error: `Script not found: getNewSongs.py`**
- Solution: Verify you're running from project root
- Check that `getNewSongs.py` and `getNewAlbums.py` exist

**Error: Albums not being liked**
- Check backend logs for "Error liking album" messages
- Verify OAuth token has proper permissions
- Test manually: `python3 getNewAlbums.py`

**Run stays in "running" status forever**
- Check backend terminal for error messages
- Query database to see error_message:
  ```bash
  sqlite3 data/app.db "SELECT * FROM runs WHERE status='running';"
  ```

### Database Issues

**Want to reset everything?**
```bash
# Stop both servers (Ctrl+C)
rm data/app.db
# Restart backend - tables will be recreated
```

**View database contents:**
```bash
sqlite3 data/app.db
.tables
SELECT * FROM runs;
SELECT * FROM songs WHERE run_id = 1;
SELECT * FROM albums WHERE run_id = 1;
.quit
```

## Next Steps

Once everything is working:

1. **Run a full weekly update**: Set hours_back to 168 (7 days)
2. **Check historical graphs**: Run multiple times to see trends
3. **Explore API docs**: http://localhost:8000/docs
4. **View past runs**: Click on any run in the history table

## Understanding the Flow

1. **Submit Run**: User enters hours → POST /api/runs/
2. **Background Task**: Scripts execute in background
3. **Polling**: Frontend polls GET /api/runs/{id} every 2 seconds
4. **Completion**: Status changes to "completed" with results
5. **History**: Stats saved to database for graphs

## Tips

- **Testing**: Use small hour values (24-48) for quick tests
- **Production runs**: Use 168 hours for weekly updates
- **Monitoring**: Watch backend logs for detailed execution info
- **Performance**: Each run takes 10-60 seconds depending on results
- **Database**: SQLite is perfect for single-user local use

## Advanced Configuration

### Environment Variables

Create a `.env` file in the backend directory to override defaults:

```env
SC_PLAYLIST_ID=your_playlist_id
SC_FILTER_MODE=activity  # or "upload" or "both"
```

### Custom Ports

**Backend on different port:**
```bash
uvicorn app.main:app --reload --port 9000
```

Update `frontend/vite.config.ts` proxy target to match.

**Frontend on different port:**
```bash
npm run dev -- --port 3000
```

Update CORS settings in `backend/app/main.py`.

## Support

If you encounter issues not covered here:

1. Check backend terminal logs
2. Check browser console (F12)
3. Review API documentation at /docs
4. Verify secrets.env and sc_token.json exist
5. Try running standalone scripts to isolate issues:
   ```bash
   python3 getNewSongs.py
   python3 getNewAlbums.py
   ```

## Security Notes

- This app is designed for **local single-user** use
- OAuth tokens stored in `sc_token.json` (keep private)
- Database at `data/app.db` (local SQLite file)
- No network exposure - localhost only
- Not suitable for multi-user deployment without authentication

## What's Next?

After successful setup, see `README_WEB_APP.md` for:
- Architecture details
- API endpoint documentation
- Development guidelines
- Database schema
- Future enhancements
