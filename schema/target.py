from typing import Optional, List
from pydantic import BaseModel, Field

class TargetBase(BaseModel):
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
    targtype1: Optional[int] = None
    targtype1_txt: Optional[str] = Field(None, description="Primary target type")
    targsubtype1: Optional[int] = None
    targsubtype1_txt: Optional[str] = Field(None, description="Primary target subtype")
    corp1: Optional[str] = Field(None, description="Primary corporate entity")
    target1: Optional[str] = Field(None, description="Primary target name")
    natlty1: Optional[int] = None
    natlty1_txt: Optional[str] = Field(None, description="Nationality of primary target")
    targtype2: Optional[int] = None
    targtype2_txt: Optional[str] = Field(None, description="Secondary target type")
    targsubtype2: Optional[int] = None
    targsubtype2_txt: Optional[str] = Field(None, description="Secondary target subtype")
    corp2: Optional[str] = Field(None, description="Secondary corporate entity")
    target2: Optional[str] = Field(None, description="Secondary target name")
    natlty2: Optional[int] = None
    natlty2_txt: Optional[str] = Field(None, description="Nationality of secondary target")
    targtype3: Optional[int] = None
    targtype3_txt: Optional[str] = Field(None, description="Tertiary target type")
    targsubtype3: Optional[int] = None
    targsubtype3_txt: Optional[str] = Field(None, description="Tertiary target subtype")
    corp3: Optional[str] = Field(None, description="Tertiary corporate entity")
    target3: Optional[str] = Field(None, description="Tertiary target name")
    natlty3: Optional[int] = None
    natlty3_txt: Optional[str] = Field(None, description="Nationality of tertiary target")

class TargetSchema(BaseModel):
    status_code: int
    status: str
    message: str
    page: int
    total_pages: int
    data: List[TargetBase]

    class Config:
        from_attributes = True