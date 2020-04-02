#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from http import HTTPStatus
from datetime import datetime
from stocker import Stocker
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
        resp = response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        return resp

def response(msg, status):
    response = {
        "statusCode" : status,
        "body" : json.dumps(msg)
    }
    return response

def get_analytics(query_params):
    incoming_date_format = "%d-%m-%Y-%H:%M"
    new_date_format = "%Y-%m-%d"

    start_date = datetime.strptime(query_params["start_date"], incoming_date_format).strftime(new_date_format)
    end_date = datetime.strptime(query_params["end_date"], incoming_date_format).strftime(new_date_format)

    symbol = query_params["symbol"]
    stock = Stocker(symbol)

    statistics = microsoft.get_stats(start_date = start_date, end_date = end_date,
                                        stats = ['Open', 'High','Low', 'Daily Change', 'Volume'])

    profit = microsoft.buy_and_hold(start_date='2012-03-01', end_date='2012-03-31')
    predict = microsoft.create_prophet_model()

    response = {
            "statusCode" : status,
            "body" : {
                "open": statistics[0],
                "high": statistics[1],
                "low": statistics[2],
                "daily_change": statistics[3],
                "volume": statistics[4],
                "profit": profit,
                "predict": predict
            }
    }

    return json.dumps(response)

def get_handler(query_params, path):
    try:
        if "analytics" in path:
            resp = get_analytics(query_params)
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
    resp = response("", HTTPStatus.NOT_FOUND)
    return resp

class RequestNotValidException(Exception):
    pass
