from fastapi import FastAPI

app = FastAPI(title="Personal Finance Tracker")

@app.get("/health")
async def health():
    return {"status": "ok"}