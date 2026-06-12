from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi_babel import Babel, BabelConfigs, BabelMiddleware

from app.api import html_routes, i18n, routes

app = FastAPI()

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
app.include_router(routes.router, prefix="/api", tags=["api"])
app.include_router(html_routes.router, tags=["html"])
app.include_router(i18n.router, tags=["i18n"])


# compile babel i18n files
if __name__ == "__main__":
    Babel(configs=babel_configs).run_cli()
