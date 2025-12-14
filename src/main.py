from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.events import router as event_router
from api.db.session import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    """
    - A "lifespan" in FastAPI means:
    Things to run when the app starts (startup)
    Things to run when the app stops (shutdown)
    - The yield separates the two phases:
    Code before yield → runs at startup
    Code after yield → runs at shutdown
    """
    init_db()
    yield


app = FastAPI(lifespan=life_span)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event_router, prefix="/api/events")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/healtz")
def read_api_health():
    return {"status":"ok"}