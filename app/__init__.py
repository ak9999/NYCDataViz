from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')  # Load configuration from config.py
# Now we can access the configuration variables via app.config["VAR_NAME"]

from app import views
