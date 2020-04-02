#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
This module provides methods to interact with
the database.
"""

from database_manager import db
from model import Favourite
from model import Portfolio
import sqlalchemy
from sqlalchemy import or_
import requests
import json

def get_user(user_id):
    user = db.query(Portfolio)\
        .filter(Portfolio.user_id == user_id)\
            .first()
    return user

def add_user(user_id):
    old_user = get_user(user_id)
    if old_user is None:
        new_user = Portfolio(user_id)
        db.add(new_user)
        return db

def get_all_favourite(user_id):
    favourite_list = db.query(Favourite)\
        .filter(Favourite.user_id == user_id)\
            .filter(Favourite.favourite_status == True)
    return favourite_list

def get_favourite(user_id, stock_symbol, favourite_status):
    favourite = db.query(Favourite)\
        .filter(Favourite.user_id == user_id)\
            .filter(Favourite.stock_symbol == stock_symbol).first()
    if favourite:
        return favourite
    else:
        return None

def delete_favourite(user_id, stock_symbol):
    favourite = db.query(Favourite)\
        .filter(Favourite.user_id == user_id)\
            .filter(Favourite.stock_symbol == stock_symbol).first()
    if favourite:
        db.delete(favourite)
        return db

# to create new entry, don't forget to check/add user first
def add_favourite(user_id, stock_symbol, favourite_status):
    old_favourite = get_favourite(user_id, stock_symbol, favourite_status)
    if old_favourite == None:
        new_favourite = Favourite(user_id, stock_symbol, favourite_status, stock_name="Null", stock_description="Null")
        db.add(new_favourite)
        return db
    else:
        return None

def get_session():
    return db
