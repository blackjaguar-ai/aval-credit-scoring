from fastapi import FastAPI

app = FastAPI(title="AVAL — Credit Scoring API")

@app.get("/health")
def health():
    return {"status": "ok", "service": "aval-api"}
