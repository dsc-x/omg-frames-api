from flask import Flask
from config import Config
from app.db import Db
from flasgger import Swagger

template = {
  "swagger": "2.0",
  "info": {
    "title": "OMG Badge Generator API",
    "description": "API Docs for the OMG Badge Generator. Link to the repo of the server [here](https://github.com/dsc-x/omg-frames-api). ",
    "contact": {
      "responsibleOrganization": "DSC-X",
      "url": "https://github.com/dsc-x",
    },
    "version": "0.0.1"
  },
  "schemes": [
    "http",
    "https"
  ],
}


app = Flask(__name__)
app.config.from_object(Config)

swagger = Swagger(app, template=template)

from app import routes


