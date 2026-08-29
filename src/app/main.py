from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi_babel import Babel, BabelConfigs, BabelMiddleware

from app.api import html_routes, i18n, routes
from app.config import USE_SAMPLE_DATA
from app.db.sample_data import init_sample_db


# lifespan
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # insert sample data
    if USE_SAMPLE_DATA:
        print("DB_PATH not exists, initializing sample data ...")
        init_sample_db()
    yield


app = FastAPI(lifespan=lifespan)

# static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# middlewares
babel_configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="",
    BABEL_TRANSLATION_DIRECTORY="../translations",
)


def locale_selector(request: Request) -> str:
    return request.cookies.get("locale") or "en"  # Fallback to "en" if no cookie is set


app.add_middleware(
    BabelMiddleware,
    babel_configs=babel_configs,
    jinja2_templates=html_routes.templates,
    locale_selector=locale_selector,
)

# router
app.include_router(routes.router, prefix="/api", tags=["API"])
app.include_router(html_routes.router, tags=["html"])
app.include_router(i18n.router, tags=["i18n"])


# compile babel i18n files
if __name__ == "__main__":
    Babel(configs=babel_configs).run_cli()
