from pydantic import BaseModel
from typing import Optional, List

class AttackBase(BaseModel):
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
    attacktype1: Optional[int] = None
    attacktype1_txt: Optional[str] = None
    attacktype2: Optional[int] = None
    attacktype2_txt: Optional[str] = None
    attacktype3: Optional[int] = None
    attacktype3_txt: Optional[str] = None
    success: Optional[int] = None
    suicide: Optional[int] = None

class AttackSchema(BaseModel):
    status_code: int
    status: str
    message: str
    page: int
    total_pages: int
    data: List[AttackBase]

    class Config:
        from_attributes = True