#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from database_manager import Base
from sqlalchemy import Table, \
Column, Integer, String, Date, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Company(Base):
    __tablename__ = 'company'
    symbol = Column(String(255), primary_key=True)
    name = Column(String(255))
    price = relationship('Price')

    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name

    def serialize(self):
        return {
            "symbol" : self.symbol,
            "name" : self.name
        }

class Price(Base):
    __tablename__ = 'price'
    date_time = Column(DateTime, primary_key=True)
    company_symbol = Column(String(255), ForeignKey('company.symbol'), primary_key=True)
    price = Column(Numeric(asdecimal=True))

    def __init__(self, company_symbol, date_time, price):
        self.company_symbol = company_symbol
        self.date_time = date_time
        self.price = price

    def serialize(self):
        return {
            "company_symbol" : self.company_symbol,
            "date_time" : datetime.strftime(self.date_time, "%d-%m-%Y-%H:%M"),
            "price" : float(self.price)
        }
