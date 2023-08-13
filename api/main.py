from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api.routes import microwave, websocket
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.include_router(microwave.router)
app.include_router(websocket.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Unhandled error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("microwave.html", {"request": request})
