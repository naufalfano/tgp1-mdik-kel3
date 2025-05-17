from typing import Optional, List
from pydantic import BaseModel

class IncidentBase(BaseModel):
    eventid: Optional[int] = None
    iyear: Optional[int] = None
    imonth: Optional[int] = None
    iday: Optional[int] = None
    country: Optional[int] = None
    country_txt: Optional[str] = None
    region: Optional[int] = None
    region_txt: Optional[str] = None
    provstate: Optional[str] = None
    city: Optional[str] = None
    summary: Optional[str] = None
    crit1: Optional[int] = None
    crit2: Optional[int] = None
    crit3: Optional[int] = None
    doubtterr: Optional[int] = None
    alternative: Optional[int] = None
    alternative_txt: Optional[str] = None
    related: Optional[str] = None

class IncidentSchema(BaseModel):
    status_code: int
    status: str
    message: str
    page: int
    total_pages: int
    data: List[IncidentBase]

    class Config:
        from_attributes = True