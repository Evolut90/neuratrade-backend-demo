from fastapi import FastAPI
import uvicorn
from app.core.config import settings


app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": f"Hello, World! {settings.api_title}"}

if __name__ == "__main__": 
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
