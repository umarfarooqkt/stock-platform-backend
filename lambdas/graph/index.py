#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from http import HTTPStatus
import requests
from datetime import datetime
import json
import pprint
import os

def handler(event, context):
    method = event.get("httpMethod")
    query_params = event.get("queryStringParameters")
    path = event.get("path").lower()
    body = event.get("body")

    try:
        if method == 'GET':
           resp = get_handler(query_params, path)
    except Exception as e:
        print("Exception_handler ",str(e))
        resp = error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        return resp

def error_response(msg, status):
    response = {
        "statusCode" : status,
        "body" : json.dumps(msg)
    }
    return response

def correct_response(graph, analysis, status):
    response = {
        "statusCode" : status,
         "headers": {
            "Access-Control-Allow-Origin": os.environ.get("ORIGIN")
        },
        "body" : {
            "graph_data": json.dumps(graph),
            "analysis": json.dumps(analysis)
        }
    }
    return response

def get_past_30_days(query_params):
    company = query_params["symbol"]
    company_data = get_company_data(company)
    if company_data:
        list_of_dates = generate_dates()
        list_of_stocks = filter_dates(company_data, list_of_dates)
        thirty_days_date = (datetime.now() - timedelta(30)).date()
        analysis_data = "This is broken"#get_analysis(company, datetime.datetime.now().date(), thirty_days_date)
        if analysis_data:
            return correct_response(list_of_stocks, analysis_data, HTTPStatus.OK)
        else:
            msg = "Error from analysis"
            return error_response(msg, HTTPStatus.INTERNAL_SERVER_ERROR)
    else:
        msg = "Company data doesn't exist"
        return error_response(msg, HTTPStatus.BAD_REQUEST)

def get_analysis(company, present_date, thirty_days_date):
    payload = { 
        "symbol": company,
        "end_date": present_date,
        "start_date": thirty_days_date
    }
    companyRequest = requests.get('https://api.cs4471-stock-platform.xyz/v1/analysis/analytics', params=payload)
    if companyRequest.status_code == 200:
        return companyRequest.json()
    else:
        return None

def filter_dates(company_data, list_of_dates):
    filtered_company_data = []
    for stock in company_data:
        datetime_object = datetime.strptime(stock["date_time"], '%d-%m-%Y-%H:%M')
        date_stock = datetime_object.date()
        if(date_stock in list_of_dates):
            filtered_company_data.append(stock)
    return filtered_company_data




def generate_dates():
    list_of_dates = []
    for i in range(0, 30):
        date = (datetime.now() - timedelta(i)).date()
        list_of_dates.append(date)
    return list_of_dates

def get_company_data(company):
    payload = { "symbol": company }
    companyRequest = requests.get('https://api.cs4471-stock-platform.xyz/v1/stock/allstocks', params=payload)
    if companyRequest.status_code == 200:
        return companyRequest.json()
    else:
        return None

def get_handler(query_params, path):
    try:
        if "ping" in path:
            resp = error_response("I am alive!", HTTPStatus.OK)
            ## gets can be added here look in index for stock service
        elif "getdatacompany" in path:
            resp = get_past_30_days(query_params)
        return resp
    except KeyError as e:
        msg = "This request is not valid " + str(e) + " " + e.args
        raise RequestNotValidException(msg)

class RequestNotValidException(Exception):
    pass
