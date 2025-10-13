from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
 
router = APIRouter(prefix="/strategies", tags=["Strategies"])