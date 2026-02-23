from fastapi import FastAPI
from src.presentation.routers.categories import router as categories_router


app = FastAPI(title="Personal Finance Tracker")
app.include_router(categories_router)


@app.get("/health")
async def health():
    return {"status": "ok"}