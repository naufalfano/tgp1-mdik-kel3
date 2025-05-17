from typing import Optional, List
from pydantic import BaseModel, Field

class PerpetratorBase(BaseModel):
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
    gname: Optional[str] = Field(None, description="Name of the group or organization")
    gsubname: Optional[str] = Field(None, description="Subname of the group")
    gname2: Optional[str] = Field(None, description="Name of second group if applicable")
    gsubname2: Optional[str] = None
    gname3: Optional[str] = Field(None, description="Name of third group if applicable")
    gsubname3: Optional[str] = None
    guncertain1: Optional[int] = Field(None, description="1 = uncertainty about first group attribution")
    guncertain2: Optional[int] = Field(None, description="1 = uncertainty about second group attribution")
    guncertain3: Optional[int] = Field(None, description="1 = uncertainty about third group attribution")
    individual: Optional[int] = Field(None, description="1 = perpetrator was an unaffiliated individual(s)")
    nperps: Optional[int] = Field(None, description="Number of perpetrators")
    nperpcap: Optional[int] = Field(None, description="Number of perpetrators captured")
    claimed: Optional[int] = Field(None, description="1 = perpetrator group claimed responsibility")
    claimmode: Optional[int] = None
    claimmode_txt: Optional[str] = Field(None, description="Method of claiming responsibility")
    claim2: Optional[int] = None
    claimmode2: Optional[int] = None
    claimmode2_txt: Optional[str] = None
    claim3: Optional[int] = None
    claimmode3: Optional[int] = None
    claimmode3_txt: Optional[str] = None
    compclaim: Optional[int] = Field(None, description="1 = competing claims of responsibility")

class PerpetratorSchema(BaseModel):
    status_code: int
    status: str
    message: str
    page: int
    total_pages: int
    data: List[PerpetratorBase]

    class Config:
        from_attributes = True