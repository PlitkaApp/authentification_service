from fastapi import FastAPI
from app.auth.router import router as router_users


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Здравствуй путник"}


app.include_router(router_users)