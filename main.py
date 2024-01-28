from fastapi import FastAPI
from config.database import engine, Base
from routers import user as user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
