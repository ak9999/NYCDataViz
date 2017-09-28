from app import app

from flask import render_template
from flask import Response
from flask import jsonify

from sodapy import Socrata

client = Socrata('data.cityofnewyork.us', None)

@app.route('/')
@app.route('/index.html')
def index():
    '''
    Returns a static webpage for now.
    '''
    return render_template('index.html')


@app.route('/demo/')
def request_demo():
    global client
    two_points = client.get('fhrw-4uyv', limit=2)
    response = Response(response=jsonify(two_points), status=200)
    return response
