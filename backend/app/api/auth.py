from fastapi import APIRouter
from ..schemas import AuthStatus
from ..services.sc_auth import SCAuthService

router = APIRouter()

@router.get("/status", response_model=AuthStatus)
async def get_auth_status():
    """
    Check SoundCloud authentication status

    Returns:
    - authenticated: bool
    - token_expires_at: datetime (if authenticated)
    - message: str (error message if not authenticated)
    """
    auth_service = SCAuthService()

    try:
        token_info = auth_service.get_token_info()

        if not token_info.get('authenticated'):
            return AuthStatus(
                authenticated=False,
                message=token_info.get('message', 'Not authenticated')
            )

        return AuthStatus(
            authenticated=True,
            token_expires_at=token_info.get('token_expires_at'),
            message=None
        )

    except Exception as e:
        return AuthStatus(
            authenticated=False,
            message=f"Authentication check failed: {str(e)}"
        )
