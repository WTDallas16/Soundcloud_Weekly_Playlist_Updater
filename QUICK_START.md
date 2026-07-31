# Quick Start Guide

## Prerequisites Check
```bash
python3 --version   # Need 3.8+
ls secrets.env      # Should exist
ls sc_token.json    # Should exist (run python3 SC_Token.py if missing)
```

## Run Locally

**Single run (7 days):**
```bash
python3 scheduled_run.py
```

**Custom period (24 hours):**
```bash
python3 scheduled_run.py --hours-back 24
```

**Original orchestrator:**
```bash
python3 runzIt.py
```

## Verify

Check the output for:
- Number of songs found and added
- Number of albums found and liked
- Database records saved to `data/app.db`

Verify database:
```bash
sqlite3 data/app.db "SELECT * FROM runs ORDER BY created_at DESC LIMIT 1;"
```

## GitHub Actions

This app runs automatically every Friday at 9:20 AM Eastern.

Manual trigger:
```bash
gh workflow run weekly-update.yml
```

Set up secrets first - see `GITHUB_ACTIONS_SETUP.md`

## Troubleshooting

**Token expired?**
```bash
python3 SC_Token.py
```

**403 Forbidden error on token refresh?**
This means your OAuth credentials are invalid or revoked.
Run `SC_Token.py` to re-authenticate with SoundCloud.

**Reset database?**
```bash
rm data/app.db
# Next run will create new database
```

## Next Steps

See detailed guides:
- `GETTING_STARTED.md` - Full setup instructions
- `GITHUB_ACTIONS_SETUP.md` - Automate with GitHub Actions
- `PROJECT_SUMMARY.md` - Architecture and implementation
