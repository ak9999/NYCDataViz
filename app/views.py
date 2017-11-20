from app import app

from flask import render_template, Response, request

import pytz
from datetime import *
from dateutil.relativedelta import *
from dateutil.parser import *

import requests

import pymongo
from bson import json_util
from os import environ


# Create connection to MongoDB cluster, and yes these are global.
try:
    key = environ['mongopass']
    client = pymongo.MongoClient(f'mongodb://mongo:{key}@citysnap-shard-00-00-dax53.mongodb.net:27017,citysnap-shard-00-01-dax53.mongodb.net:27017,citysnap-shard-00-02-dax53.mongodb.net:27017/test?ssl=true&replicaSet=citysnap-shard-0&authSource=admin')
    db = client.database
    collection = db.requests
    collection.create_index([('unique_key', pymongo.DESCENDING)], unique=True)
except Exception as e:
    print('Exception:', e)


# Temporarily here to print out data from database.
@app.route('/cursor')
def print_collection():
    global collection
    projection = {'_id': False, 'unique_key': True, 'created_date': True, 'descriptor': True}
    cursor = collection.find({}, projection).sort('created_date', pymongo.DESCENDING)

    return render_template('cursor.html', count=collection.count(), cursor=cursor)


def store_retrieved_data(service_requests):
    # service_requests: a list filled with JSON documents.
    global collection
    '''
    TODO:
    # Build a list of unique_key from service_requests
    unique_key_list = [key['unique_key'] for key in service_requests]
    '''
    try:
        collection.insert_many(service_requests, ordered=False)
    except Exception as e:
        print("Exception:", e)


@app.route('/')
@app.route('/index')
def index():
    '''
    Returns a static webpage for now.
    '''
    return render_template('index.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/query')
def request_data():
    # These are the desired columns:
    # ['Unique Key', 'Latitude', 'Longitude', 'Created Date', 'Agency', 'Agency Name', 'Complaint Type', 'Descriptor']
    columns = "unique_key,latitude,longitude,created_date,agency,agency_name,complaint_type,descriptor"

    # Get recent service requests
    eastern_tz = pytz.timezone('US/Eastern')  # Generate time zone from string.
    today = datetime.now()  # Generate datetime object right now.
    today = today.astimezone(eastern_tz)  # Convert today to new datetime
    time_delta = today - relativedelta(days=3)

    # Convert datetimes into Floating Timestamps for use with Socrata.
    today = today.strftime('%Y-%m-%d') + 'T00:00:00'
    time_delta = time_delta.strftime('%Y-%m-%d') + 'T00:00:00'

    '''
    GET request on Socrata's API.
    First part is the data set we're using.
    $limit is set to the maximum number of records we want.
    $select will select the columns we want, as defined earlier.
    $where allows us to choose the time frame. In this case it's 6 weeks.
    '''
    api_url = "https://data.cityofnewyork.us/resource/fhrw-4uyv.json?"
    filters = {
        '$limit': 50000,
        '$select': columns,
        '$where': f'created_date between \'{time_delta}\' and \'{today}\'' +
            'and longitude is not null'
    }
    agency = request.args.get('agency')
    complaint_type = request.args.get('type')
    if agency is not None:
        # Append the agency to the API url for searching.
        api_url += f'agency={agency}'
    if complaint_type is not None:
        # Update the filter with a full text search of the data set.
        filters.update({'$q': f'\'{complaint_type}\''})

    r = requests.get(api_url, params=filters)
    store_retrieved_data(r.json())

    # Create the response
    response = Response(response=r, status=200, mimetype='application/json')
    return response
