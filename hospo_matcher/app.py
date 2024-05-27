from fastapi import FastAPI

from hospo_matcher.routers import sessions

app = FastAPI()

app.include_router(sessions.router)


@app.get("/")
async def root():
    return {"message": "API is running."}
