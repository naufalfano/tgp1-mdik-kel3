from fastapi import Depends, HTTPException, status, APIRouter, Query, Request
from http import HTTPStatus
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from models import *
from schema import *
import math

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

async def result(model_class, db: AsyncSession, page, limit, filters=None, sorting=None):
    try:
        query = select(model_class)
        if filters:
            valid_columns = model_class.__table__.columns.keys()
            invalid_filters = [k for k in filters if k not in valid_columns]
            if invalid_filters:
                handle_error("invalid_filter", invalid_filters)
            for attr, value in filters.items():
                if value is not None and hasattr(model_class, attr):
                    query = query.where(getattr(model_class, attr) == value)

        if sorting:
            sort_by = sorting.get("sort_by")
            order = sorting.get("order", "asc")
            if sort_by:
                if sort_by not in model_class.__table__.columns.keys():
                    handle_error("invalid_sort", sort_by)
                sort_column = getattr(model_class, sort_by)
                sort_column = sort_column.desc() if order == "desc" else sort_column.asc()
                query = query.order_by(sort_column)
        
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await db.execute(count_query)
        total_items = count_result.scalar() or 0

        offset = (page - 1) * limit
        total_pages = math.ceil(total_items / limit)
        paginated_results = query.offset(offset).limit(limit)
        result = await db.execute(paginated_results)
        results = result.scalars().all()
        
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
async def root():
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
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    return await result (Attack, db, pagination["page"], pagination["limit"], filters, sorting)

@router.get("/api/casualties", response_model=CasualtiesSchema)
async def get_casualties(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    return await result (Casualties, db, pagination["page"], pagination["limit"], filters, sorting)

@router.get("/api/incident", response_model=IncidentSchema)
async def get_incident(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    return await result (Incident, db, pagination["page"], pagination["limit"], filters, sorting)

@router.get("/api/perpetrator", response_model=PerpetratorSchema)
async def get_perpetrator(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    return await result (Perpetrator, db, pagination["page"], pagination["limit"], filters, sorting)

@router.get("/api/target", response_model=TargetSchema)
async def get_target(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    return await result (Target, db, pagination["page"], pagination["limit"], filters, sorting)

@router.get("/api/weapon", response_model=WeaponSchema)
async def get_weapon(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_filters()),
    sorting: dict = Depends(get_sorting)
):
    return await result (Weapon, db, pagination["page"], pagination["limit"], filters, sorting)
