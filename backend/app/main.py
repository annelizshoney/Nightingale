from fastapi import FastAPI

app = FastAPI(
    title="Nightingale API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Nightingale backend is running"
    }