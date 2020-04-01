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
from sqlalchemy import or_, and_

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

def get_all_unfavourite(user_id):
    favourite_list = db.query(Favourite)\
        .filter(Favourite.user_id == user_id)\
            .filter(or_(
                Favourite.favourite_status == False,
                Favourite.favourite_status == None))
    return favourite_list

# to create new entry, don't forget to check/add user first
def add_favourite(user_id, stock_symbol, favourite_status):
    old_favourite = db.query(Portfolio)\
        .filter(Favourite.user_id == user_id)\
            .filter(Favourite.stock_symbol == stock_symbol).first()
    if old_favourite is None:
        new_favourite = Portfolio(user_id, stock_symbol, favourite_status, stock_name="Null", stock_description="Null")
        db.add(new_favourite)
        return db
    else:
        return None

## this can be used to change fav status
def update_favourite_status(user_id, stock_symbol, new_favourite_status):
    favourite_search = db.query(Portfolio)\
        .filter(Favourite.user_id == user_id)\
            .filter(and_(
                Favourite.stock_symbol == stock_symbol
            ))
    if favourite_search is not None:
        db.query(Portfolio)\
            .filter(Favourite.user_id == user_id)\
                .filter(and_(
                    Favourite.stock_symbol == stock_symbol
                    )).update({"favourite_status": new_favourite_status})
        return db

def get_session():
    return db
