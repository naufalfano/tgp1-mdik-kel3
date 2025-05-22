from fastapi import HTTPException, status, Query, Request
from http import HTTPStatus
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models import *
from schema import *
import math

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

async def result(model_class, db: AsyncSession, page: int, limit: int, filters=None, sorting=None):
    try:
        query = select(model_class)

        if filters:
            valid_columns = model_class.__table__.columns.keys()
            for attr, value in filters.items():
                if value is not None and attr in valid_columns:
                    query = query.where(getattr(model_class, attr) == value)

        if sorting:
            sort_by = sorting.get("sort_by")
            if sort_by and sort_by in model_class.__table__.columns.keys():
                order = sorting.get("order", "asc")
                column = getattr(model_class, sort_by)
                query = query.order_by(column.desc() if order == "desc" else column.asc())

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await db.execute(count_query)
        total_items = count_result.scalar()

        # Pagination
        offset = (page - 1) * limit
        total_pages = math.ceil(total_items / limit)
        paginated_result = query.offset(offset).limit(limit)

        # Execute query
        result = await db.execute(paginated_result)
        results = result.scalars().all()

        # Serialize results
        serialized_results = []
        for item in results:
            item_dict = {}
            for column in model_class.__table__.columns:
                item_dict[column.name] = getattr(item, column.name)
            serialized_results.append(item_dict)

        return {
            "status_code": status.HTTP_200_OK,
            "status": "Success",
            "message": "Data fetched successfully",
            "page": page,
            "total_pages": total_pages,
            "data": serialized_results
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )