from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from database import engine, Base
import models
import routers

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(routers.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return RedirectResponse(url="/static/index.html")