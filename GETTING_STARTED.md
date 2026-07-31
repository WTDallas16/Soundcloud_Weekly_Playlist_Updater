# Getting Started with SoundCloud Weekly Updater

This guide will help you set up and run the SoundCloud automation system.

## Prerequisites

Before starting, ensure you have:

1. **Python 3.8+** installed
   ```bash
   python3 --version
   ```

2. **SoundCloud OAuth credentials** in `secrets.env`:
   ```env
   SC_CLIENT_ID=your_client_id_here
   SC_CLIENT_SECRET=your_client_secret_here
   ```

3. **Valid OAuth token** in `sc_token.json`:
   - If you don't have this, run: `python3 SC_Token.py`
   - Follow the OAuth flow to generate your token

## Installation

### Step 1: Install Python Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Verify OAuth Token

```bash
# Check if you have a valid token
ls sc_token.json

# If not, generate one:
python3 SC_Token.py
```

## Quick Start

### Run a Single Update

```bash
# Full week (7 days)
python3 scheduled_run.py

# Custom period (24 hours)
python3 scheduled_run.py --hours-back 24
```

### Verify Results

Check the output for:
- Number of songs found and added
- Number of albums found and liked
- Database records saved

View the database:
```bash
sqlite3 data/app.db
SELECT * FROM runs ORDER BY created_at DESC LIMIT 1;
.quit
```

## GitHub Actions Setup (Recommended)

For automatic weekly runs via GitHub Actions, see [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md).

This provides:
- Automatic execution every Friday at 9:20 AM Eastern
- Manual trigger capability
- Automatic token refresh and persistence
- Artifact tracking

## Troubleshooting

### Token Issues

**Error: Token file not found**
```bash
python3 SC_Token.py
```

**Error: 403 Forbidden on token refresh**
This means your OAuth credentials are invalid or revoked. Run:
```bash
python3 SC_Token.py
```

**Token expired mid-run**
The app automatically refreshes tokens 5 minutes before expiry, but if you see expiry errors:
```bash
python3 SC_Token.py
```

### Database Issues

**Reset database:**
```bash
rm data/app.db
# Next run will create new database
```

**View all runs:**
```bash
sqlite3 data/app.db "SELECT id, created_at, hours_back, songs_count, albums_count, status FROM runs ORDER BY created_at DESC LIMIT 10;"
```

**View songs from a run:**
```bash
sqlite3 data/app.db "SELECT track_title, uploader_username FROM songs WHERE run_id = 1;"
```

### Script Execution Issues

**Error: Script not found**
- Verify you're running from the project root directory
- Check that `getNewSongs.py` and `getNewAlbums.py` exist

**Albums not being liked**
- Check backend logs for error messages
- Verify OAuth token has proper permissions
- Test manually: `python3 getNewAlbums.py`

**Run fails with unclear error**
- Check the error_message in the database:
  ```bash
  sqlite3 data/app.db "SELECT error_message FROM runs WHERE id = (SELECT MAX(id) FROM runs);"
  ```

## Configuration

### Environment Variables

Set these in `secrets.env`:

```env
SC_CLIENT_ID=your_client_id
SC_CLIENT_SECRET=your_client_secret

# Optional overrides
SC_PLAYLIST_ID=1907305003
SC_FILTER_MODE=activity  # or "upload" or "both"
```

### Filter Modes

- **activity** (default): Filters by when tracks appeared in your feed
- **upload**: Filters by actual upload time
- **both**: Requires both timestamps to be within the window

## Advanced Usage

### Original Scripts

If you want to run the original standalone scripts:

```bash
# Run everything (songs + albums)
python3 runzIt.py

# Run songs only
python3 getNewSongs.py

# Run albums only
python3 getNewAlbums.py
```

### Backend API (Development)

For development or testing, you can run the FastAPI backend:

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Then test endpoints:
```bash
curl http://localhost:8000/api/health
curl http://localhost:8000/api/auth/status
```

## Understanding the Flow

1. **CLI Execution**: `scheduled_run.py` starts and loads OAuth token
2. **Token Refresh**: Checks if token expires soon, refreshes if needed
3. **Script Execution**: Dynamically imports and runs getNewSongs.py and getNewAlbums.py
4. **Data Collection**: Gathers songs and albums with metadata
5. **Database Save**: Records all results to SQLite database
6. **Exit Code**: Returns 0 on success, 1 on failure

## Database Schema

```sql
-- Run execution records
runs (id, created_at, hours_back, start_time, end_time, status,
      songs_count, albums_count, error_message, duration_seconds)

-- Songs found in each run
songs (id, run_id, track_id, track_title, track_permalink_url,
       uploader_username, uploaded_at, activity_created_at)

-- Albums found and liked in each run
albums (id, run_id, playlist_id, title, playlist_type, permalink_url,
        uploader, track_count, activity_created_at, liked)
```

## Tips

- **Testing**: Use `--hours-back 24` for quick tests (10-30 seconds)
- **Production runs**: Use `--hours-back 168` for full weekly updates (30-90 seconds)
- **Monitoring**: Watch the console output for detailed execution info
- **Database**: Query `sqlite3 data/app.db` to review historical data
- **Token management**: Automatic refresh happens on every run

## Support

If you encounter issues not covered here:

1. Check console output for error messages
2. Review database error_message column:
   ```bash
   sqlite3 data/app.db "SELECT error_message FROM runs ORDER BY created_at DESC LIMIT 1;"
   ```
3. Try running standalone scripts to isolate issues:
   ```bash
   python3 getNewSongs.py
   python3 getNewAlbums.py
   ```
4. Verify secrets.env and sc_token.json exist and are valid

## What's Next?

- **Automation**: See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for scheduling
- **Details**: See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture
- **API**: See [backend/requirements.txt](backend/requirements.txt) for dependencies

## Security Notes

- This app is designed for **local single-user** use
- OAuth tokens stored in `sc_token.json` (keep private, don't commit to git)
- Database at `data/app.db` (local SQLite file)
- For GitHub Actions: Use repository secrets (SC_SECRETS_ENV, SC_TOKEN_JSON)
- Not suitable for multi-user deployment without authentication
