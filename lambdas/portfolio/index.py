#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from http import HTTPStatus
import json
import pprint
import methods as db
from database_manager import ORIGIN 

def handler(event, context):
    method = event.get("httpMethod")
    query_params = event.get("queryStringParameters")
    path = event.get("path")
    if path:
        path = path.lower()
    
    body = event.get("body")
    records = event.get("Records")
    print(event)

    print(body)

    #SNS
    if records:
        user_id = json.loads(json.loads(records[0]["body"])["Message"])["sub"]
        try:
            session = create_user(user_id)
            session.commit()
        except Exception as e:
            print("Exception_handler ",str(e))
            db.get_session().rollback()
        finally:
            db.get_session().close()
            return

    user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
    #HTTP
    try:
        if method == 'GET':
           resp = get_handler(query_params, path, user_id)
        elif method == 'POST':
            resp = post_handler(body, path, user_id)
    except Exception as e:
        print("Exception_handler ",str(e))
        db.get_session().rollback()
        resp = response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db.get_session().close()
        return resp

def create_user(user_id):
    created_user = db.add_user(user_id)
    if created_user:
        return created_user
    else:
        msg = "User already exists with id " + user_id
        raise Exception(msg)

def response(msg, status):
    response = {
        "header": {
            "origin": ORIGIN
        }
        "statusCode" : status,
        "body" : json.dumps(msg)
    }
    return response

def get_all_favourites(query_params, user_id):
    favourite_list = db.get_all_favourite(user_id)
    if favourite_list:
        resp = response(serialize_list(favourite_list), HTTPStatus.OK)
    else:
        resp = response(favourite_list, HTTPStatus.NOT_FOUND)
    return resp

def get_all_unfavourites(query_params, user_id):
    unfavourite_list = db.get_all_unfavourite(user_id)
    if unfavourite_list:
        resp = response(serialize_list(unfavourite_list), HTTPStatus.OK)
    else:
        resp = response(unfavourite_list, HTTPStatus.NOT_FOUND)
    return resp

def get_user_portfolio(query_params, user_id):
    user_id_portfolio = db.get_user(user_id)
    if user_id_portfolio:
        resp = response(user_id_portfolio.serialize(), HTTPStatus.OK)
    else:
        resp = response(user_id_portfolio, HTTPStatus.NOT_FOUND)
    return resp

def add_favourite(body, user_id):
    stock_symbol = body["stock_symbol"]
    status = body["favourite_status"]
    added_favourite = db.get_favourite(user_id)
    if added_favourite:
        return db.add_favourite(user_id, stock_symbol, status)
    else:
        msg = "Company with symbol " + stock_symbol + " not found"
        raise Exception(msg)

def update_favourite(body, user_id):
    stock_symbol = body["stock_symbol"]
    status = body["update_favourite_status"]
    updated_favourite = db.get_favourite(user_id)
    if updated_favourite:
        return db.update_favourite_status(user_id, stock_symbol, status)
        
    else:
        msg = "Company with symbol " + stock_symbol + " not found"
        raise Exception(msg)

def get_handler(query_params, path, user_id):
    try:
        if "ping" in path:
            resp = response("I am alive!", HTTPStatus.OK)
            ## gets can be added here look in index for stock service
        elif "allfavourites" in path:
            resp = get_all_favourites(query_params, user_id)
        elif "allunfavourites" in path:
            resp = get_all_unfavourites(query_params, user_id)
        elif "getportfolio" in path:
            resp = get_user_portfolio(query_params, user_id)
        else:
            msg = "The '" + path + "' is not supported"
            resp = response(msg, HTTPStatus.BAD_REQUEST)
        return resp
    except KeyError as e:
        msg = "This request is not valid " + str(e) + " " + e.args
        raise RequestNotValidException(msg)

def post_handler(body, path, user_id):
    body = json.loads(body)
    if "addfavourite" in path:
        ## posts can be added here look at handler in stock service
        session = add_favourite(body, user_id)
    if "updatefavourite" in path:
        session = update_favourite(body, user_id)
    else:
        msg = "The '" + path + "' is not supported"
        resp = response(msg, HTTPStatus.BAD_REQUEST)
        return resp
    session.commit()
    msg = "success!"
    resp = response(msg, HTTPStatus.CREATED)
    return resp

def serialize_list(data_list):
    serialized_data_list = []
    for i in data_list:
        serialized_data_list.append(i.serialize())
    return serialized_data_list

class RequestNotValidException(Exception):
    pass
