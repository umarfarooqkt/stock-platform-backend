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

def get_handler(query_params, path):
    try:
        if "ping" in path:
            resp = response("I am alive!", HTTPStatus.OK)
            ## gets can be added here look in index for stock service
        else:
            msg = "The '" + path + "' is not supported"
            resp = response(msg, HTTPStatus.BAD_REQUEST)
        return resp
    except KeyError as e:
        msg = "This request is not valid " + str(e) + " " + e.args
        raise RequestNotValidException(msg)

def post_handler(body, path):
    body = json.loads(body)
    if "favourite" in path:
        ## posts can be added here look at handler in stock service
        pass
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