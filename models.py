from sqlalchemy import Column, Integer, String, Float
from database import Base

class Holding(Base):
    __table_name__ = "holdings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True),
    Ticker = Column(String, nullable=False),
    HoldingType = Column(String),
    HoldingSize = Column(Float),
    DateAdded = Column(String)

    def __repr__(self):
        return f"<Holdings(id='{self.id}', Ticker='{self.Ticker}', HoldingType='{self.HoldingType}', HoldingSize='{self.HoldingSize}', DateAdded='{self.DateAdded}')>"



