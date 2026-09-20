from fastapi import FastAPI

app = FastAPI(title="Steward Control Plane")


@app.get("/health")
async def health():
    return {"status": "ok"}
