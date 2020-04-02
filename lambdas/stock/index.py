#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from http import HTTPStatus
from datetime import datetime
import methods as db
import json
import pprint

def handler(event, context):
    method = event.get("httpMethod")
    query_params = event.get("queryStringParameters")
    path = event.get("path").lower()
    body = event.get("body")

    try:
        if method == 'GET':
           resp = get_handler(query_params, path)
        elif method == 'POST':
            resp = post_handler(body, path)
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

def get_company(query_params):
    company = db.get_company(query_params["symbol"])
    if company:
        resp = response(company.serialize(), HTTPStatus.OK)
    else:
        resp = response(company, HTTPStatus.NOT_FOUND)
    return resp

def get_quote(query_params):
    date_time = datetime.strptime(query_params["date_time"], "%d-%m-%Y-%H:%M")
    price = db.get_price(query_params["symbol"], date_time)
    if price:
        resp = response(price.serialize(), HTTPStatus.OK)
    else:
        msg = "No quote found"
        resp = response(msg, HTTPStatus.NOT_FOUND)
    return resp

def get_all_stocks(query_params):
    company = db.get_all_price_for_company(query_params["symbol"])
    if company:
        resp = response(serialize_list(company), HTTPStatus.OK)
    else:
        resp = response(company, HTTPStatus.NOT_FOUND)
    return resp

def post_quote(body):
    date_time = datetime.strptime(body["date_time"], "%d-%m-%Y-%H:%M")
    price = body.get("price")
    symbol = body["symbol"]
    check_company = db.get_company(symbol)
    if check_company:
        return db.add_price(symbol, date_time, price)
    else:
        msg = "Company with symbol " + symbol + " not found"
        raise Exception(msg)

def post_company(body):
    symbol = body["symbol"]
    name = body.get("name")
    return db.add_company(symbol, name)

def get_handler(query_params, path):
    try:
        if "quote" in path:
            resp = get_quote(query_params)
        elif "company" in path:
            resp = get_company(query_params)
        elif "allstock" in path:
            resp = get_all_stocks(query_params)
        elif "ping" in path:
            resp = response("I am alive!", HTTPStatus.OK)
        else:
            msg = "The '" + path + "' is not supported"
            resp = response(msg, HTTPStatus.BAD_REQUEST)
        return resp
    except KeyError as e:
        msg = "This request is not valid " + str(e) + " " + e.args
        raise RequestNotValidException(msg)

def post_handler(body, path):
    body = json.loads(body)
    if "quote" in path:
        session = post_quote(body)
    elif "company" in path:
        session = post_company(body)
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