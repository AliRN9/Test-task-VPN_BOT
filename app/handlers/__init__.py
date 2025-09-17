from app.handlers.default import default_router
from app.handlers.remnawave import remnawave_router

routers_list = [default_router, remnawave_router]
__all__ = ['default_router']
