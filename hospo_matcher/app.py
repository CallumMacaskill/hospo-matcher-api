from fastapi import FastAPI

from hospo_matcher.routers import sessions, venues

app = FastAPI()

app.include_router(sessions.router)
app.include_router(venues.router)


@app.get("/")
async def root():
    return {"message": "API is running."}
