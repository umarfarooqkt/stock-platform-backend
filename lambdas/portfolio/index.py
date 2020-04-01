#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from http import HTTPStatus
import json
import pprint
import methods as db

def handler(event, context):
    method = event.get("httpMethod")
    query_params = event.get("queryStringParameters")
    path = event.get("path").lower()
    body = event.get("body")
    user_id = event["authorizer"]["claim"]["sub"]

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

def response(msg, status):
    response = {
        "statusCode" : status,
        "body" : json.dumps(msg)
    }
    return response

def get_all_favourites(query_params, user_id):
    favourite_list = db.get_all_favourite(user_id)
    if favourite_list:
        resp = response(favourite_list.serialize(), HTTPStatus.OK)
    else:
        resp = response(favourite_list, HTTPStatus.NOT_FOUND)
    return resp

def get_all_unfavourites(query_params, user_id):
    unfavourite_list = db.get_all_unfavourite(user_id)
    if unfavourite_list:
        resp = response(unfavourite_list.serialize(), HTTPStatus.OK)
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
    added_favourite = db.get_user(user_id)
    if added_favourite:
        return db.add_favourite(user_id, stock_symbol, status)
    else:
        msg = "Company with symbol " + stock_symbol + " not found"
        raise Exception(msg)

def update_favourite(body, user_id):
    stock_symbol = body["stock_symbol"]
    status = body["favourite_status"]
    added_favourite = db.get_user(user_id)
    if added_favourite:
        return db.add_favourite(user_id, stock_symbol, status)
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
        elif "portfolio" in path:
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
        resp = add_favourite(body, user_id)
    if "updatefavourite" in path:
        resp = update_favourite(body, user_id)
    else:
        msg = "The '" + path + "' is not supported"
        resp = response(msg, HTTPStatus.BAD_REQUEST)
        return resp
    db.get_session().commit()
    msg = "success!"
    resp = response(msg, HTTPStatus.CREATED)
    return resp

class RequestNotValidException(Exception):
    pass