import unittest
import os
import shutil
import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
from io import StringIO

#import sys; print(list(sys.modules.keys()))
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create folder for test uploads
        os.mkdir(upload_path())

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())

    def test_get_songs(self):
        file_A = models.File(name='file_A.mp3')
        song_A = models.Song(file_=file_A)
        file_B = models.File(name='file_B.mp3')
        song_B = models.Song(file_=file_B)

        session.add_all([file_A, file_B, song_A, song_B])
        session.commit()

        response = self.client.get(
            '/api/songs',
            headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')

        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 2)

        response_song_A, response_song_B = data
        self.assertEqual(response_song_A['id'], song_A.id)
        self.assertEqual(response_song_A['file']['id'], song_A.file_.id)
        self.assertEqual(response_song_A['file']['name'], song_A.file_.name)
        self.assertEqual(response_song_B['id'], song_B.id)
        self.assertEqual(response_song_B['file']['id'], song_B.file_.id)
        self.assertEqual(response_song_B['file']['name'], song_B.file_.name)
