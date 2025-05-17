from sqlalchemy import Column, Integer, String, Text, ForeignKey, BigInteger
from config.database import Base

class Incident(Base):
    __tablename__ = "incident"

    incident_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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
    summary = Column(Text, nullable=True)
    crit1 = Column(Integer, nullable=True)
    crit2 = Column(Integer, nullable=True)
    crit3 = Column(Integer, nullable=True)
    doubtterr = Column(Integer, nullable=True)
    alternative = Column(Integer, nullable=True)
    alternative_txt = Column(String(256), nullable=True)
    related = Column(Text, nullable=True)
