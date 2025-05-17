from typing import Optional, List
from pydantic import BaseModel

class CasualtiesBase(BaseModel):
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
    nkill: Optional[float] = None
    nkillus: Optional[float] = None
    nkillter: Optional[float] = None
    nwound: Optional[float] = None
    nwoundus: Optional[float] = None
    nwoundte: Optional[float] = None
    property: Optional[int] = None
    propextent: Optional[int] = None
    propextent_txt: Optional[str] = None
    propvalue: Optional[float] = None
    propcomment: Optional[str] = None
    ishostkid: Optional[int] = None
    nhostkid: Optional[int] = None
    nhostkidus: Optional[int] = None
    nhours: Optional[int] = None
    ndays: Optional[int] = None
    divert: Optional[str] = None
    kidhijcountry: Optional[str] = None
    ransom: Optional[int] = None
    ransomamt: Optional[float] = None
    ransomamtus: Optional[float] = None
    ransompaid: Optional[float] = None
    ransompaidus: Optional[float] = None
    ransomnote: Optional[str] = None
    hostkidoutcome: Optional[int] = None
    hostkidoutcome_txt: Optional[str] = None
    nreleased: Optional[int] = None

class CasualtiesSchema(BaseModel):
    status_code: int
    status: str
    message: str
    page: int
    total_pages: int
    data: List[CasualtiesBase]

    class Config:
        from_attributes = True