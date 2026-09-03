from fastapi import FastAPI
app = FastAPI()

from src.routes import auth_router
app.include_router(auth_router)


