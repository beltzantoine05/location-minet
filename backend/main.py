from fastapi import FastAPI

app = FastAPI(title="location MiNET API")

@app.get("/")

def read_root():
    return {"message": "Bienvenu sur l'API de location MiNET"}
