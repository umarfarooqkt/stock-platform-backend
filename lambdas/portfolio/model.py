#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from database_manager import Base
from sqlalchemy import Table, \
Column, Boolean, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

"""
Portfolio exists so users don't need a stock
entry to persist
"""
class Portfolio(Base):
    __tablename__ = 'portfolio'
    user_id = Column(String(255), primary_key=True)

    def __init__(self, user_id):
        self.user_id = user_id

    def serialize(self):
        return {
            "user_id" : self.user_id
        }
        
class Favourite(Base):
    __tablename__ = 'favourite'
    user_id = Column(String(255), ForeignKey('portfolio.user_id'), primary_key=True)
    stock_symbol = Column(String(255), primary_key=True)
    stock_name = Column(String(255))
    stock_description = Column(String(255))
    favourite_status = Column(Boolean, unique=False)

    def __init__(self, user_id, stock_symbol, favourite_status, 
        stock_name, stock_description):
        self.user_id = user_id
        self.stock_symbol = stock_symbol
        self.favourite_status = favourite_status
        self.stock_name = stock_name
        self.stock_description = stock_description

    def serialize(self):
        return {
            "user_id" : self.user_id,
            "stock_symbol" : self.stock_symbol,
            "favourite_status" : self.favourite_status,
            "stock_name" : self.stock_name,
            "stock_description" : self.stock_description
        }

import database_manager
Base.metadata.create_all(database_manager.engine)
