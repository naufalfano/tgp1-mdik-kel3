from fastapi import Depends, HTTPException, status, APIRouter, Query, Request
from http import HTTPStatus
from sqlalchemy.orm import Session
from config.database import get_db
from config.redis import r
from models import *
from schema import *
import math
import json

router = APIRouter()

def get_pagination(
    page: int = Query(None, ge=1, description="Page number"),
    limit: int = Query(None, ge=1, description="Items per page"),
):
    PAGE_DEFAULT: int = 1
    LIMIT_DEFAULT: int = 100
    return {
        "page": page or PAGE_DEFAULT,
        "limit": limit or LIMIT_DEFAULT
    }

def get_filters():
    def get_filters_dep(request: Request):
        exclude_keys = {"page", "limit", "sort_by", "order"}
        return {
            k: v for k, v in request.query_params.items()
            if k not in exclude_keys
        }
    return get_filters_dep

def get_sorting(
    sort_by: str = Query(None, description="Sort by column name"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Sort order: asc or desc"),
):
    return {
        "sort_by": sort_by,
        "order": order,
    }

def handle_error(error_type: str, data=None):
    messages = {
        "invalid_filter": {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": lambda data, code: f"{code} {HTTPStatus(code).phrase}: Invalid filter column(s): {', '.join(data)}"
        },
        "invalid_sort": {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": lambda data, code: f"{code} {HTTPStatus(code).phrase}: Invalid sort column: {data}"
        },
        "not_found": {
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": lambda data, code: (
                f"{code} {HTTPStatus(code).phrase}: No data found for {data}" if data
                else f"{code} {HTTPStatus(code).phrase}: No data found"
            )
        },
        "internal_error": {
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": lambda data, code: f"{code} {HTTPStatus(code).phrase}: Internal Server Error: {data}"
        }
    }

    if error_type not in messages:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unhandled error type"
        )

    config = messages[error_type]
    code = config["status_code"]
    raise HTTPException(
        status_code=code,
        detail=config["message"](data, code)
    )

def result(model_class, db, page, limit, filters=None, sorting=None):
    try:
        query = db.query(model_class)
        if filters:
            valid_columns = model_class.__table__.columns.keys()
            invalid_filters = [k for k in filters if k not in valid_columns]
            if invalid_filters:
                handle_error("invalid_filter", invalid_filters)
            for attr, value in filters.items():
                if value is not None and hasattr(model_class, attr):
                    query = query.filter(getattr(model_class, attr) == value)

        if sorting:
            sort_by = sorting.get("sort_by")
            order = sorting.get("order", "asc")
            if sort_by:
                if sort_by not in model_class.__table__.columns.keys():
                    handle_error("invalid_sort", sort_by)
                sort_column = getattr(model_class, sort_by)
                sort_column = sort_column.desc() if order == "desc" else sort_column.asc()
                query = query.order_by(sort_column)
        
        total_items = query.count()
        offset = (page - 1) * limit
        total_pages = math.ceil(total_items / limit)
        results = query.offset(offset).limit(limit).all()
        
        if not results:
            query_info = {}
            if filters:
                query_info.update({k: v for k, v in filters.items() if v is not None})
            handle_error("not_found", data=query_info)
        
        return {
            "status_code": status.HTTP_200_OK,
            "status": "Success",
            "message": "Data fetched successfully",
            "page": page,
            "total_pages": total_pages,
            "data": results
        }
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        handle_error("internal_error", str(e))

@router.get("/")
def root():
    return {"message":"type '/docs' for documentation"}

@router.get("/api", response_model=CaseSchema)
async def get_case(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)

):
    return result (Case, db, pagination["page"], pagination["limit"], filters, sorting)

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

### REDIS ENDPOINT ###

@router.get("/redis/api/", response_model=CaseSchema)
async def get_case_redis(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    cache_key = f"case:{pagination['page']}:{pagination['limit']}:{str(filters)}:{str(sorting)}"
    
    cached_result = r.get(cache_key)
    if cached_result:
        try:
            return json.loads(cached_result)
        except Exception as e:
            print(f"Cache deserialization error: {str(e)}")
    
    data = result(Case, db, pagination["page"], pagination["limit"], filters, sorting)
    serialized_data = {
        "status_code": data["status_code"],
        "status": data["status"],
        "message": data["message"],
        "page": data["page"],
        "total_pages": data["total_pages"]
    }
    
    serialized_items = []
    for item in data["data"]:
        item_dict = {}
        for column in Case.__table__.columns:
            column_name = column.name
            item_dict[column_name] = getattr(item, column_name)
        serialized_items.append(item_dict)
    
    serialized_data["data"] = serialized_items
    
    try:
        r.setex(cache_key, 300, json.dumps(serialized_data, default=str))
    except Exception as e:
        print(f"Redis cache error: {e}")

    return serialized_data

@router.get("/redis/api/attack", response_model=AttackSchema)
async def get_attack_redis(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    cache_key = f"attack:{pagination['page']}:{pagination['limit']}:{str(filters)}:{str(sorting)}"
    
    cached_result = r.get(cache_key)
    if cached_result:
        try:
            return json.loads(cached_result)
        except Exception as e:
            print(f"Cache deserialization error: {str(e)}")
    
    data = result(Attack, db, pagination["page"], pagination["limit"], filters, sorting)
    serialized_data = {
        "status_code": data["status_code"],
        "status": data["status"],
        "message": data["message"],
        "page": data["page"],
        "total_pages": data["total_pages"]
    }
    
    serialized_items = []
    for item in data["data"]:
        item_dict = {}
        for column in Attack.__table__.columns:
            column_name = column.name
            item_dict[column_name] = getattr(item, column_name)
        serialized_items.append(item_dict)
    
    serialized_data["data"] = serialized_items
    
    try:
        r.setex(cache_key, 300, json.dumps(serialized_data, default=str))
    except Exception as e:
        print(f"Redis cache error: {e}")

    return serialized_data

@router.get("/redis/api/casualties", response_model=CasualtiesSchema)
async def get_casualties_redis(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    cache_key = f"casualties:{pagination['page']}:{pagination['limit']}:{str(filters)}:{str(sorting)}"
    
    cached_result = r.get(cache_key)
    if cached_result:
        try:
            return json.loads(cached_result)
        except Exception as e:
            print(f"Cache deserialization error: {str(e)}")
    
    data = result(Casualties, db, pagination["page"], pagination["limit"], filters, sorting)
    serialized_data = {
        "status_code": data["status_code"],
        "status": data["status"],
        "message": data["message"],
        "page": data["page"],
        "total_pages": data["total_pages"]
    }
    
    serialized_items = []
    for item in data["data"]:
        item_dict = {}
        for column in Casualties.__table__.columns:
            column_name = column.name
            item_dict[column_name] = getattr(item, column_name)
        serialized_items.append(item_dict)
    
    serialized_data["data"] = serialized_items
    
    try:
        r.setex(cache_key, 300, json.dumps(serialized_data, default=str))
    except Exception as e:
        print(f"Redis cache error: {e}")

    return serialized_data

@router.get("/redis/api/incident", response_model=IncidentSchema)
async def get_incident_redis(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    cache_key = f"incident:{pagination['page']}:{pagination['limit']}:{str(filters)}:{str(sorting)}"
    
    cached_result = r.get(cache_key)
    if cached_result:
        try:
            return json.loads(cached_result)
        except Exception as e:
            print(f"Cache deserialization error: {str(e)}")
    
    data = result(Incident, db, pagination["page"], pagination["limit"], filters, sorting)
    serialized_data = {
        "status_code": data["status_code"],
        "status": data["status"],
        "message": data["message"],
        "page": data["page"],
        "total_pages": data["total_pages"]
    }
    
    serialized_items = []
    for item in data["data"]:
        item_dict = {}
        for column in Incident.__table__.columns:
            column_name = column.name
            item_dict[column_name] = getattr(item, column_name)
        serialized_items.append(item_dict)
    
    serialized_data["data"] = serialized_items
    
    try:
        r.setex(cache_key, 300, json.dumps(serialized_data, default=str))
    except Exception as e:
        print(f"Redis cache error: {e}")

    return serialized_data

@router.get("/redis/api/perpetrator", response_model=PerpetratorSchema)
async def get_perpetrator_redis(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    cache_key = f"perpetrator:{pagination['page']}:{pagination['limit']}:{str(filters)}:{str(sorting)}"
    
    cached_result = r.get(cache_key)
    if cached_result:
        try:
            return json.loads(cached_result)
        except Exception as e:
            print(f"Cache deserialization error: {str(e)}")
    
    data = result(Perpetrator, db, pagination["page"], pagination["limit"], filters, sorting)
    serialized_data = {
        "status_code": data["status_code"],
        "status": data["status"],
        "message": data["message"],
        "page": data["page"],
        "total_pages": data["total_pages"]
    }
    
    serialized_items = []
    for item in data["data"]:
        item_dict = {}
        for column in Perpetrator.__table__.columns:
            column_name = column.name
            item_dict[column_name] = getattr(item, column_name)
        serialized_items.append(item_dict)
    
    serialized_data["data"] = serialized_items
    
    try:
        r.setex(cache_key, 300, json.dumps(serialized_data, default=str))
    except Exception as e:
        print(f"Redis cache error: {e}")

    return serialized_data

@router.get("/redis/api/target", response_model=TargetSchema)
async def get_target_redis(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    cache_key = f"target:{pagination['page']}:{pagination['limit']}:{str(filters)}:{str(sorting)}"
    
    cached_result = r.get(cache_key)
    if cached_result:
        try:
            return json.loads(cached_result)
        except Exception as e:
            print(f"Cache deserialization error: {str(e)}")
    
    data = result(Target, db, pagination["page"], pagination["limit"], filters, sorting)
    serialized_data = {
        "status_code": data["status_code"],
        "status": data["status"],
        "message": data["message"],
        "page": data["page"],
        "total_pages": data["total_pages"]
    }
    
    serialized_items = []
    for item in data["data"]:
        item_dict = {}
        for column in Target.__table__.columns:
            column_name = column.name
            item_dict[column_name] = getattr(item, column_name)
        serialized_items.append(item_dict)
    
    serialized_data["data"] = serialized_items
    
    try:
        r.setex(cache_key, 300, json.dumps(serialized_data, default=str))
    except Exception as e:
        print(f"Redis cache error: {e}")

    return serialized_data

@router.get("/redis/api/weapon", response_model=WeaponSchema)
async def get_weapon_redis(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    cache_key = f"weapon:{pagination['page']}:{pagination['limit']}:{str(filters)}:{str(sorting)}"
    
    cached_result = r.get(cache_key)
    if cached_result:
        try:
            return json.loads(cached_result)
        except Exception as e:
            print(f"Cache deserialization error: {str(e)}")
    
    data = result(Weapon, db, pagination["page"], pagination["limit"], filters, sorting)
    serialized_data = {
        "status_code": data["status_code"],
        "status": data["status"],
        "message": data["message"],
        "page": data["page"],
        "total_pages": data["total_pages"]
    }
    
    serialized_items = []
    for item in data["data"]:
        item_dict = {}
        for column in Weapon.__table__.columns:
            column_name = column.name
            item_dict[column_name] = getattr(item, column_name)
        serialized_items.append(item_dict)
    
    serialized_data["data"] = serialized_items
    
    try:
        r.setex(cache_key, 300, json.dumps(serialized_data, default=str))
    except Exception as e:
        print(f"Redis cache error: {e}")

    return serialized_data
