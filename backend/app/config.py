from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # SoundCloud API credentials
    sc_client_id: str
    sc_client_secret: str

    # Optional overrides
    sc_playlist_id: str = "1907305003"
    sc_filter_mode: str = "activity"

    # Paths
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    token_file: Path = base_dir / "sc_token.json"
    database_url: str = f"sqlite:///{base_dir}/data/app.db"

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent.parent / "secrets.env")
        env_prefix = ""
        case_sensitive = False

settings = Settings()
