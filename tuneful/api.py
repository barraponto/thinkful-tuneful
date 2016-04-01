import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from tuneful import app
from .database import session
from .utils import upload_path

@app.route('/api/songs', methods=['GET'])
@decorators.accept("application/json")
def get_songs():
    data = session.query(models.Song)

    data = data.order_by(models.Song.id)
    return Response(json.dumps([song.as_dict() for song in data]),
                    200, mimetype='application/json')
