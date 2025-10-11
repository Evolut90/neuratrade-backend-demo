from fastapi import FastAPI
import uvicorn
from app.core.config import settings
from api.routes.market import router as market_router


app = FastAPI(title=settings.api_title,
    version=settings.api_version,
    description="Sistema de trading automatizado com IA",
    debug=settings.debug) 
    
app.include_router(market_router)

@app.get("/")
async def read_root():
    return {"message": f"Hello, World! {settings.api_title}"}

if __name__ == "__main__": 
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
