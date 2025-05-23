from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, BigInteger
from config.database import Base

class Casualties(Base):
    __tablename__ = "casualties"

    casualties_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    eventid = Column(BigInteger, ForeignKey("case.eventid"), index=True)
    iyear = Column(Integer, nullable=True, index=True)
    imonth = Column(Integer, nullable=True, index=True)
    iday = Column(Integer, nullable=True, index=True)
    country = Column(Integer, nullable=True, index=True)
    country_txt = Column(String(256), nullable=True, index=True)
    region = Column(Integer, nullable=True, index=True)
    region_txt = Column(String(256), nullable=True, index=True)
    provstate = Column(String(256), nullable=True, index=True)
    city = Column(String(256), nullable=True, index=True)
    nkill = Column(Float, index=True, nullable=True)
    nkillus = Column(Float, nullable=True)
    nkillter = Column(Float, nullable=True)
    nwound = Column(Float, index=True, nullable=True)
    nwoundus = Column(Float, nullable=True)
    nwoundte = Column(Float, nullable=True)
    property = Column(Integer, index=True, nullable=True)
    propextent = Column(Integer, nullable=True)
    propextent_txt = Column(String(256), nullable=True)
    propvalue = Column(Float, nullable=True)
    propcomment = Column(Text, nullable=True)
    ishostkid = Column(Integer, index=True, nullable=True)
    nhostkid = Column(Integer, nullable=True)
    nhostkidus = Column(Integer, nullable=True)
    nhours = Column(Integer, nullable=True)
    ndays = Column(Integer, nullable=True)
    divert = Column(String(256), nullable=True)
    kidhijcountry = Column(String(256), nullable=True)
    ransom = Column(Integer, index=True, nullable=True)
    ransomamt = Column(Float, nullable=True)
    ransomamtus = Column(Float, nullable=True)
    ransompaid = Column(Float, nullable=True)
    ransompaidus = Column(Float, nullable=True)
    ransomnote = Column(Text, nullable=True)
    hostkidoutcome = Column(Integer, index=True, nullable=True)
    hostkidoutcome_txt = Column(String(256), nullable=True)
    nreleased = Column(Integer, nullable=True)