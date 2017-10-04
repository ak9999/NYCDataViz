from app import app

from flask import render_template
from flask import Response
from sodapy import Socrata

import json

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
    query_data = client.get('fhrw-4uyv', limit=200, select=columns)

    # Create the response
    response = Response(response=json.dumps(query_data), status=200, mimetype='application/json')
    return response
