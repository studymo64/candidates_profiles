from fastapi import FastAPI
# from .routes import router
from .routes import router

app = FastAPI()
# app.include_router(router)
app.include_router(router)
