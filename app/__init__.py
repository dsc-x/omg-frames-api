"""
  app package
  ~~~~~~~~~~~

  This package contains the main logic of the app. It initialises

  - Flask App
  - Mail service
  - Swagger

  Modules:
  - db
  - routes
"""

from flask import Flask
from config import Config
from app.db import Db
from flasgger import Swagger
from flask_cors import CORS
from flask_mail import Mail

template = {
  "swagger": "2.0",
  "info": {
    "title": "iWasAt Events API",
    "description": "API Docs for the iWasAt Events. Link to the repo of the server [here](https://github.com/dsc-x/omg-frames-api). ",
    "contact": {
      "responsibleOrganization": "DSC-X",
      "url": "https://iwasat.events",
    },
    "version": "0.0.1"
  },
  "schemes": [
    "http",
    "https"
  ],
  'securityDefinitions': {
    'basicAuth': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'}
  }
}


app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
mail = Mail(app)
swagger = Swagger(app, template=template)

from app import routes
