#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# Imports

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Constants

DB_OVERRIDE = os.environ.get("DB_OVERRIDE")
ORIGIN = os.environ.get("ORIGIN")
RDS_SECRET_ARN = os.environ.get("RDS_SECRET_ARN")
AWS_REGION = os.environ.get("AWS_REGION")
MYSQL_CONNECTOR = 'mysql+mysqlconnector'

if DB_OVERRIDE:
    host = DB_OVERRIDE
    user = 'root'
    password = 'abcd123'
    database = 'stock'
    port = '3306'
    log = False
else:
    host = 'localhost'
    host =  "docker.for.mac.localhost"
    user = 'root'
    password = 'abcd123'
    database = 'stock'
    port = '3306'
    log = True

# Create database connection

connection_credentials = MYSQL_CONNECTOR + '://' + user + ':' + password + '@' + host + ':' + port + '/' + database
engine = create_engine(connection_credentials, echo=log)
Base = declarative_base()
Session = sessionmaker(bind=engine)
db = Session()

# Utility methods

def create_database_schema(engine):
   """
    Create database schema and 
    create relational mapping
   :param database:
   :return: void
   """
   Base.metadata.create_all(engine)
