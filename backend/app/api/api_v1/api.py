from fastapi import APIRouter

from . import auth, dashboard, inventory, projects, tickets, users, wikis

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(wikis.router, prefix="/wikis", tags=["wikis"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
