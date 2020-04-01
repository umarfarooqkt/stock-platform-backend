#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
This module provides methods to interact with
the database.
"""

from database_manager import db
from model import Company
from model import Price
import sqlalchemy

def get_company(symbol):
    company = db.query(Company)\
        .filter(Company.symbol == symbol).first()
    return company

def add_company(symbol, name=None):
    old_company = get_company(symbol)
    if old_company is None:
        company = Company(symbol, name)
        db.add(company)
        return db
    else:
        return None

def get_price(symbol, date_time):
    price = db.query(Price)\
        .filter(Price.company_symbol == symbol)\
            .filter(Price.date_time == date_time).first()
    return price

def add_price(symbol, date_time, price):
    old_price = get_price(symbol, date_time)
    if old_price is None:
        price = Price(symbol, date_time, price)
        db.add(price)
        return db
    else:
        return None

def get_all_price_for_company(symbol):
    stock_list = db.query(Price)\
        .filter(Price.company_symbol == symbol)
    return stock_list

def get_session():
    return db
