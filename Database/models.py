from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from Database.database import Base
from datetime import datetime
# from Stock import Stock

class Holding(Base): # all owned holdings (each transaction)
    __tablename__ = "holdings"

    holding_id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.ticker_id"))
    holding_size = Column(Float, nullable=False)
    account_name = Column(String, ForeignKey("accounts.account_name"))
    date_added = Column(Date, nullable=True)
    date_edited = Column(Date, nullable=True)

    ticker = relationship("Ticker", back_populates="holdings")
    account = relationship("Account", back_populates="holdings")

    # def to_stock(self):
    #     return Stock(ticker=self.ticker, holding_type=self.holdingType, quantity=self.holdingSize)

    def __repr__(self):
        return (f"<Holdings(id='{self.holding_id}', Ticker='{self.ticker.ticker_name}', Holding Type="
                f"'{self.ticker.type}', "f"Holding Size='{self.holding_size}', Date Added='{self.date_added}', Date "
                f"Edited='{self.date_edited}')>")


class Ticker(Base):
    __tablename__ = "tickers"

    ticker_id = Column(Integer, primary_key=True)
    ticker_name = Column(String, unique=True, nullable=False)
    type = Column(String)
    price = Column(Integer)

    holdings = relationship("Holding", back_populates="ticker", cascade="all, delete-orphan")


class Account(Base):
    __tablename__ = "accounts"

    account_name = Column(String, primary_key=True)
    account_type = Column(String)

    holdings = relationship("Holding", back_populates="account", cascade="all, delete-orphan")