from fastapi import FastAPI
from . import routes

app = FastAPI()

# Include the router for user registration
app.include_router(routes.router)


@app.get("/")
def root():
    return {"message": "Welcome to Taxation API"}
