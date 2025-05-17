from typing import Optional, List
from pydantic import BaseModel, Field

class WeaponBase(BaseModel):
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
    weaptype1: Optional[int] = None
    weaptype1_txt: Optional[str] = Field(None, description="Primary weapon type")
    weapsubtype1: Optional[int] = None
    weapsubtype1_txt: Optional[str] = Field(None, description="Primary weapon subtype")
    weaptype2: Optional[int] = None
    weaptype2_txt: Optional[str] = Field(None, description="Secondary weapon type")
    weapsubtype2: Optional[int] = None
    weapsubtype2_txt: Optional[str] = Field(None, description="Secondary weapon subtype")
    weaptype3: Optional[int] = None
    weaptype3_txt: Optional[str] = Field(None, description="Tertiary weapon type")
    weapsubtype3: Optional[int] = None
    weapsubtype3_txt: Optional[str] = Field(None, description="Tertiary weapon subtype")
    weaptype4: Optional[int] = None
    weaptype4_txt: Optional[str] = Field(None, description="Quaternary weapon type")
    weapsubtype4: Optional[int] = None
    weapsubtype4_txt: Optional[str] = Field(None, description="Quaternary weapon subtype")
    weapdetail: Optional[str] = Field(None, description="Additional weapon details")

class WeaponSchema(BaseModel):
    status_code: int
    status: str
    message: str
    page: int
    total_pages: int
    data: List[WeaponBase]

    class Config:
        from_attributes = True