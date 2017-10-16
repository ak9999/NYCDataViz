from app import app

from flask import render_template
from flask import Response

from dateutil.relativedelta import *
from dateutil.parser import *

import requests

from datetime import *

@app.route('/')
@app.route('/index.html')
def index():
    '''
    Returns a static webpage for now.
    '''
    return render_template('index.html')


@app.route('/query/')
def request():
    # These are the desired columns:
    # ['Latitude', 'Longitude', 'Created Date', 'Agency', 'Agency Name', 'Complaint Type', 'Descriptor']
    columns = "latitude,longitude,created_date,agency,agency_name,complaint_type,descriptor"

    # Get recent service requests (last 6 weeks)
    today = date.today()
    six_weeks_ago = today - relativedelta(weeks=6)
    # Convert datetimes into Floating Timestamps for use with Socrata.
    today = today.strftime('%Y-%m-%d') + 'T00:00:00'
    six_weeks_ago = six_weeks_ago.strftime('%Y-%m-%d') + 'T00:00:00'

    '''
    GET request on Socrata's API.
    First part is the data set we're using.
    $limit is set to 500K, because we want 500K records.
    $select will select the columns we want, as defined earlier.
    $where allows us to choose the time frame. In this case it's 6 weeks.
    '''
    r = requests.get(
        "https://data.cityofnewyork.us/resource/fhrw-4uyv.json?" +
        "$limit=500000&$select={}&".format(columns) +
        "$where=created_date between \'{}\' and \'{}\' and longitude IS NOT NULL".format(six_weeks_ago, today)
    )

    # Create the response
    response = Response(response=r, status=200, mimetype='application/json')
    return response
