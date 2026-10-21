

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="NC+1 API")

def run():
    uvicorn.run("src.app:app", reload=True)
