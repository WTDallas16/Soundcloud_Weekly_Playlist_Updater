# SoundCloud Weekly Updater - Web Application

A FastAPI + React web interface for the SoundCloud automation scripts. This application provides a user-friendly dashboard to run your SoundCloud weekly updates, view results in real-time, and track historical data with graphs.

## Features

- **Web Dashboard**: Clean, intuitive interface to trigger runs
- **Real-Time Results**: Live polling shows run progress and results
- **Historical Graphs**: Visual representation of songs/albums over time
- **Database Tracking**: SQLite database stores all run history
- **Automatic Token Refresh**: OAuth tokens refresh automatically before expiry
- **Background Processing**: Runs execute in background without blocking the UI

## Architecture

- **Backend**: FastAPI with SQLAlchemy (SQLite)
- **Frontend**: React + TypeScript + Vite + TailwindCSS + Recharts
- **Authentication**: SoundCloud OAuth with automatic token refresh
- **Script Integration**: Wraps existing `getNewSongs.py` and `getNewAlbums.py` without modifications

## Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify secrets.env exists in project root
# It should contain:
# SC_CLIENT_ID=your_client_id
# SC_CLIENT_SECRET=your_client_secret

# Verify sc_token.json exists in project root
# Generate it using: python3 SC_Token.py (if needed)

# Start the backend server
uvicorn app.main:app --reload --port 8000
```

The backend will:
- Initialize the SQLite database at `data/app.db`
- Create all necessary tables automatically
- Start the API server on http://localhost:8000
- Serve API documentation at http://localhost:8000/docs

### 2. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will start on http://localhost:5173

### 3. Access the Application

1. Open your browser to http://localhost:5173
2. Verify the authentication status indicator (green dot = authenticated)
3. Start a new run by entering hours to look back (default: 168 hours = 7 days)
4. Watch the results appear in real-time
5. View historical graphs and past runs below

## API Endpoints

### Runs
- `POST /api/runs/` - Create and start a new run
- `GET /api/runs/{id}` - Get run details (for polling)
- `GET /api/runs/` - List recent runs

### History
- `GET /api/history/stats` - Get statistics for graphing

### Auth
- `GET /api/auth/status` - Check authentication status

### Health
- `GET /api/health` - Health check endpoint

## How It Works

### Script Execution Flow

1. User submits run form with `hours_back` parameter
2. Backend creates a Run record with `status='running'`
3. Background task executes:
   - Dynamically imports `getNewSongs.py` and `getNewAlbums.py`
   - Injects authenticated `SCClient` via monkey-patching
   - Calls internal functions to fetch songs and albums
   - Likes albums automatically
   - Saves results to database
4. Frontend polls every 2 seconds until `status='completed'`
5. Results displayed with songs/albums tables

### Token Refresh Strategy

- Tokens checked before every API call
- Automatic refresh if expiry < 5 minutes away
- New token saved to `sc_token.json`
- No manual intervention required

### Database Schema

**runs** table:
- Run metadata (status, counts, duration, errors)

**songs** table:
- Track details (title, artist, URLs, timestamps)
- Foreign key to runs

**albums** table:
- Playlist details (title, type, tracks, like status)
- Foreign key to runs

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate

# Run with auto-reload
uvicorn app.main:app --reload --port 8000

# View logs in terminal
```

### Frontend Development

```bash
cd frontend

# Development server with HMR
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Database Management

```bash
# View database contents
sqlite3 data/app.db

# Common queries
SELECT * FROM runs ORDER BY created_at DESC LIMIT 10;
SELECT COUNT(*) FROM songs WHERE run_id = 1;
SELECT * FROM albums WHERE liked = 'yes';
```

## Troubleshooting

### Backend Issues

**Import Error: No module named 'soundAuthen'**
- This is expected - the app reimplements SCClient
- Verify `backend/app/services/sc_client.py` exists

**Token Expired**
- Check `sc_token.json` exists in project root
- Regenerate tokens: `python3 SC_Token.py`

**Database Errors**
- Delete `data/app.db` and restart backend
- Tables will be recreated automatically

### Frontend Issues

**CORS Errors**
- Verify backend is running on port 8000
- Check CORS settings in `backend/app/main.py`

**Polling Never Completes**
- Check backend logs for errors
- Verify run status in database: `SELECT * FROM runs WHERE id = X;`

**Blank Page**
- Check browser console for errors
- Verify all dependencies installed: `npm install`

## Standalone Scripts Still Work

The existing scripts remain fully functional:

```bash
# Run songs only
python3 getNewSongs.py

# Run albums only
python3 getNewAlbums.py

# Run both (original workflow)
python3 runzIt.py
```

No modifications to these scripts are required or made.

## Future Enhancements

Potential improvements:
- WebSocket support for real-time updates (instead of polling)
- Export run results to CSV/JSON
- Email notifications on run completion
- Configurable filter modes (activity/upload/both)
- Multiple playlist support
- User authentication (if multi-user deployment)
- Docker containerization

## Technical Notes

- SQLite is perfect for single-user local deployment
- Background tasks use FastAPI's BackgroundTasks
- Frontend uses Axios for HTTP requests
- Recharts for responsive graphs
- TailwindCSS for styling (no custom CSS needed)
- TypeScript for type safety
- Vite for fast development builds

## Support

For issues or questions:
1. Check backend logs in terminal
2. Check frontend console in browser DevTools
3. Verify `secrets.env` and `sc_token.json` exist
4. Review API docs at http://localhost:8000/docs
