from sqlalchemy import Column, Integer, String, Float, Date
from Database.database import Base

# from Stock import Stock

class Holding(Base): # all owned holdings (each transaction)
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=False)
    holdingType = Column(String, nullable=True)
    holdingSize = Column(Float, nullable=False)
    dateAdded = Column(Date, nullable=True)
    dateEdited = Column(Date, nullable=True)

    def __repr__(self):
        return (f"<Holdings(id='{self.id}', Ticker='{self.ticker}', Holding Type='{self.holdingType}', Holding Size="
                f"'{self.holdingSize}', Date Added='{self.dateAdded}', Date Edited='{self.dateEdited}')>")

    # def to_stock(self):
    #     return Stock(ticker=self.ticker, holding_type=self.holdingType, quantity=self.holdingSize)

