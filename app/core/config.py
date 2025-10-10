from pydantic_settings import BaseSettings
from typing import Optional 

 
class Settings(BaseSettings): 
    
    # API Settings
    api_title: str = "AI Trading Bot - NeuraTrade"
    api_version: str = "1.0.0"
    debug: bool = True
    
    # Database
    database_url: Optional[str] = None
    redis_url: str = "redis://localhost:6379"
    
    # Trading APIs
    binance_api_key: Optional[str] = None
    binance_secret_key: Optional[str] = None
    
    # ML Settings
    model_save_path: str = "data/models"
    historical_data_path: str = "data/historical"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
  
settings = Settings()