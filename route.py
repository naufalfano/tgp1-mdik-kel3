from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from config.redis import r
from models import *
from schema import *
import time
from controller.response import get_filters, get_pagination, get_sorting, result
from controller.caching import compress_data, decompress_data

router = APIRouter()


@router.get("/")
def root():
    return {"message":"type '/docs' for documentation"}

@router.get("/api", response_model=CaseSchema)
async def get_case(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)

):
    return await result (Case, db, pagination["page"], pagination["limit"], filters, sorting)

@router.get("/api/attack", response_model=AttackSchema)
async def get_attack(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    return result (Attack, db, pagination["page"], pagination["limit"], filters, sorting)

@router.get("/api/casualties", response_model=CasualtiesSchema)
async def get_casualties(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    return result (Casualties, db, pagination["page"], pagination["limit"], filters, sorting)

@router.get("/api/incident", response_model=IncidentSchema)
async def get_incident(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    return result (Incident, db, pagination["page"], pagination["limit"], filters, sorting)

@router.get("/api/perpetrator", response_model=PerpetratorSchema)
async def get_perpetrator(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    return result (Perpetrator, db, pagination["page"], pagination["limit"], filters, sorting)

@router.get("/api/target", response_model=TargetSchema)
async def get_target(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    return result (Target, db, pagination["page"], pagination["limit"], filters, sorting)

@router.get("/api/weapon", response_model=WeaponSchema)
async def get_weapon(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    return result (Weapon, db, pagination["page"], pagination["limit"], filters, sorting)


@router.get("/redis/api", response_model=CaseSchema)
async def get_case_redis(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    cache_key = f"case:{pagination['page']}:{pagination['limit']}:{str(filters)}:{str(sorting)}"
    compression_flag_key = f"{cache_key}:compressed"
    
    # Try to get from cache
    try:        

        pipe = await r.pipeline()
        await pipe.get(cache_key)
        await pipe.get(compression_flag_key)
        cached_result, is_compressed_flag = await pipe.execute()
        
        if cached_result:
            is_compressed = is_compressed_flag == '1' if is_compressed_flag else False
            
            decompressed_data = decompress_data(cached_result, is_compressed)
            
            print(f"Cache retrieved (compressed: {is_compressed})")
            return decompressed_data
            
    except Exception as e:
        print(f"Cache retrieval error: {(e)}")
    
    # Fetch from database
    print("Fetching data from db")
    data = await result(Case, db, pagination["page"], pagination["limit"], filters, sorting)
    
    # Store in cache with smart compression
    try:        
        data_str, is_compressed = compress_data(data)
        
        # Store both data and compression flag
        pipe = await r.pipeline()
        await pipe.setex(cache_key, 300, data_str)
        await pipe.setex(compression_flag_key, 300, '1' if is_compressed else '0')
        await pipe.execute()
        
        print(f"Data successfully cached (compressed: {is_compressed})")
        
    except Exception as e:
        print(f"Caching data failed: {(e)}")

    return data