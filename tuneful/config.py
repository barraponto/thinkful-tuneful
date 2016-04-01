class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://postgres@localhost:5432/tf-tuneful"
    DEBUG = True
    UPLOAD_FOLDER = "uploads"

class TestingConfig(object):
    DATABASE_URI = "postgresql://postgres@localhost:5432/tf-tuneful-tests"
    DEBUG = True
    UPLOAD_FOLDER = "test-uploads"
