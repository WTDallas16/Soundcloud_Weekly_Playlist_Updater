# SoundCloud Weekly Song Updater

This project automates your weekly SoundCloud workflow:

- finds new songs from followed artists
- finds new albums and likes them
- updates your target playlist
- stores run history in SQLite
- runs automatically via GitHub Actions (scheduled weekly or manual trigger)

## Project Structure

- [runzIt.py](/Users/WillyTardif/Documents/Claude_SC_Weekly_Song_Updater/runzIt.py): original weekly runner
- [scheduled_run.py](/Users/WillyTardif/Documents/Claude_SC_Weekly_Song_Updater/scheduled_run.py): headless runner for automation and GitHub Actions
- [getNewSongs.py](/Users/WillyTardif/Documents/Claude_SC_Weekly_Song_Updater/getNewSongs.py): fetches new tracks and updates the playlist
- [getNewAlbums.py](/Users/WillyTardif/Documents/Claude_SC_Weekly_Song_Updater/getNewAlbums.py): finds albums and likes them
- [backend](/Users/WillyTardif/Documents/Claude_SC_Weekly_Song_Updater/backend): Database models and OAuth token management

## Requirements

- Python 3.8+
- SoundCloud OAuth credentials in `secrets.env`
- A valid token in `sc_token.json`

Example `secrets.env`:

```env
SC_CLIENT_ID=your_client_id
SC_CLIENT_SECRET=your_client_secret
```

Optional overrides:

```env
SC_PLAYLIST_ID=1907305003
SC_FILTER_MODE=activity
```

## Local Usage

### Headless Run (Recommended)

Run the weekly job:

```bash
python3 scheduled_run.py
```

Run with a custom window:

```bash
python3 scheduled_run.py --hours-back 168
```

### Original Scripts

```bash
python3 runzIt.py
python3 getNewSongs.py
python3 getNewAlbums.py
```

## GitHub Actions Automation

This repo includes a scheduled workflow at [weekly-update.yml](/Users/WillyTardif/Documents/Claude_SC_Weekly_Song_Updater/.github/workflows/weekly-update.yml) that runs every Friday at 9:00 AM Eastern.

To enable it, add these GitHub repository secrets:

- `SC_SECRETS_ENV`
- `SC_TOKEN_JSON`
- `GH_ACTIONS_SECRET_PAT` optional, for saving refreshed tokens back to GitHub

Full setup steps are in [GITHUB_ACTIONS_SETUP.md](/Users/WillyTardif/Documents/Claude_SC_Weekly_Song_Updater/GITHUB_ACTIONS_SETUP.md).

## Data and State

- `albums_added.txt` tracks which albums have already been liked
- `data/app.db` stores run history for the dashboard
- `sc_token.json` stores the SoundCloud OAuth token state

Keep `secrets.env` and `sc_token.json` private.

## Additional Docs

- [QUICK_START.md](/Users/WillyTardif/Documents/Claude_SC_Weekly_Song_Updater/QUICK_START.md)
- [GETTING_STARTED.md](/Users/WillyTardif/Documents/Claude_SC_Weekly_Song_Updater/GETTING_STARTED.md)
- [GITHUB_ACTIONS_SETUP.md](/Users/WillyTardif/Documents/Claude_SC_Weekly_Song_Updater/GITHUB_ACTIONS_SETUP.md)

- Updated for headless mode 07/31/2026