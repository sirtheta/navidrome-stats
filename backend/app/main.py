from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import html_routes, routes

app = FastAPI()

# static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# router
app.include_router(routes.router, prefix="/api", tags=["api"])
app.include_router(html_routes.router, tags=["html"])
