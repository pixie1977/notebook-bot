from .start_router import router as start_router
from .weather_router import router as weather_router
from .crypto_router import router as crypto_router
from .form_router import router as form_router

__all__ = [
    "start_router",
    "weather_router",
    "crypto_router",
    "form_router",
]