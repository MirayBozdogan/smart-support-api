from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_database
from routers.tickets import router as tickets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield


app = FastAPI(title="Smart Support API", lifespan=lifespan)
app.include_router(tickets_router)


@app.get("/")
def home():
    return {"message": "Smart Support API çalışıyor."}
