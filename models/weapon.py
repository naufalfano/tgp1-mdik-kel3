from sqlalchemy import Column, Integer, String, Text, ForeignKey, BigInteger
from config.database import Base

class Weapon(Base):
    __tablename__ = "weapon"

    weapon_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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
    weaptype1 = Column(Integer, index=True, nullable=True)
    weaptype1_txt = Column(String(256), index=True, nullable=True)
    weapsubtype1 = Column(Integer, index=True, nullable=True)
    weapsubtype1_txt = Column(String(256), nullable=True)
    weaptype2 = Column(Integer, nullable=True)
    weaptype2_txt = Column(String(256), nullable=True)
    weapsubtype2 = Column(Integer, nullable=True)
    weapsubtype2_txt = Column(String(256), nullable=True)
    weaptype3 = Column(Integer, nullable=True)
    weaptype3_txt = Column(String(256), nullable=True)
    weapsubtype3 = Column(Integer, nullable=True)
    weapsubtype3_txt = Column(String(256), nullable=True)
    weaptype4 = Column(Integer, nullable=True)
    weaptype4_txt = Column(String(256), nullable=True)
    weapsubtype4 = Column(Integer, nullable=True)
    weapsubtype4_txt = Column(String(256), nullable=True)
    weapdetail = Column(Text, nullable=True)
