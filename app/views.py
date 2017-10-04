from app import app

from flask import render_template
from flask import Response

from sodapy import Socrata

from dateutil.relativedelta import *
from dateutil.parser import *

import requests

import json
from datetime import *

client = Socrata('data.cityofnewyork.us', None)

@app.route('/')
@app.route('/index.html')
def index():
    '''
    Returns a static webpage for now.
    '''
    return render_template('index.html')


@app.route('/query/')
def request():
    # Refer to globally defined client variable.
    global client
    # These are the desired columns:
    # ['Latitude', 'Longitude', 'Created Date', 'Agency', 'Agency Name', 'Complaint Type', 'Descriptor']

    columns = "latitude,longitude,created_date,agency,agency_name,complaint_type,descriptor"

    # Get recent service requests (last 6 weeks)
    today = date.today()
    six_weeks_ago = today - relativedelta(weeks=6)
    today = today.strftime('%Y-%m-%d') + 'T00:00:00'
    six_weeks_ago = six_weeks_ago.strftime('%Y-%m-%d') + 'T00:00:00'
    # today = today.strftime('%Y-%m-%d')
    # six_weeks_ago = six_weeks_ago.strftime('%Y-%m-%d')
    print(today)
    print(six_weeks_ago)
    # query_data = client.get('fhrw-4uyv', select=columns,
    #                         where="created_date between {} and {}".format(six_weeks_ago, today))

    # r = requests.get(
    #     "https://data.cityofnewyork.us/resource/fhrw-4uyv.json?" +
    #     "$where=created_date between \'{}\' and \'{}\',".format(six_weeks_ago, today) +
    #     "$select={}".format(columns)
    # )

    r = requests.get(
        "https://data.cityofnewyork.us/resource/fhrw-4uyv.json?$query=" +
        "SELECT {} WHERE".format(columns) +
        " created_date between \'{}\' and \'{}\'".format(six_weeks_ago, today)
    )

    # Create the response
    # response = Response(response=json.loads(query_data), status=200, mimetype='application/json')
    response = Response(response=r, status=200, mimetype='application/json')
    return response
