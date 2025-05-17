from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from config.database import Base

class Attack(Base):
    __tablename__ = "attack"

    attack_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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
    attacktype1 = Column(Integer, index=True, nullable=True)
    attacktype1_txt = Column(String(256), index=True, nullable=True)
    attacktype2 = Column(Integer, nullable=True)
    attacktype2_txt = Column(String(256), nullable=True)
    attacktype3 = Column(Integer, nullable=True)
    attacktype3_txt = Column(String(256), nullable=True)
    success = Column(Integer, index=True, nullable=True)
    suicide = Column(Integer, index=True, nullable=True)
