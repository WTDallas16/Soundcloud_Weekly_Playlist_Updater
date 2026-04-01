# GitHub Actions Weekly Automation

This project can run automatically in GitHub Actions every Friday at 9:00 AM Eastern without starting the frontend or backend servers.

## What was added

- `scheduled_run.py` runs the same SoundCloud workflow headlessly
- `.github/workflows/weekly-update.yml` schedules the job
- `getNewAlbums.py` now uses the repo's `albums_added.txt` file instead of a hardcoded local path

## Schedule

GitHub cron uses UTC, so the workflow includes:

- `0 13 * * 5`
- `0 14 * * 5`

It then checks the actual `America/New_York` time and only continues at Friday 9:00 AM Eastern. That keeps it correct across daylight saving time changes.

## Required GitHub Secrets

Add these repository secrets before enabling the workflow:

### `SC_SECRETS_ENV`

Paste the full contents of your local `secrets.env`, for example:

```env
SC_CLIENT_ID=your_client_id
SC_CLIENT_SECRET=your_client_secret
```

You can also include optional overrides there like:

```env
SC_PLAYLIST_ID=1907305003
SC_FILTER_MODE=activity
```

### `SC_TOKEN_JSON`

Paste the full contents of your local `sc_token.json`.

This lets the workflow start with your current SoundCloud token state.

### Optional: `GH_ACTIONS_SECRET_PAT`

If you want refreshed SoundCloud tokens written back into the `SC_TOKEN_JSON` GitHub secret after each run, create a personal access token that can manage repository secrets and store it as `GH_ACTIONS_SECRET_PAT`.

If you skip this secret, the workflow still runs, but a rotated refresh token in `sc_token.json` would not automatically be saved back to GitHub for the next scheduled run.

## Manual Runs

The workflow also supports `workflow_dispatch`, so you can trigger it from GitHub manually.

- Leave `hours_back` blank to use the existing weekly calculation from `runzIt.py`
- Enter a value like `168` if you want an exact rolling 7-day window

## State That Gets Preserved

- `albums_added.txt` is committed back to the repo automatically when it changes
- `data/app.db` is uploaded as a workflow artifact, but not committed

If you want the SQLite history database persisted between runs too, that can be added later.
