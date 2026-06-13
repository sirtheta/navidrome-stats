from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

router: APIRouter = APIRouter()


@router.get("/set-locale/{lang}")
async def set_locale(lang: str, request: Request):
    referer = request.headers.get("referer") or "/"
    response = RedirectResponse(url=referer)
    response.set_cookie(
        key="locale", value=lang, max_age=60 * 60 * 24 * 30
    )  # Cookie lasts for 30 days
    return response
