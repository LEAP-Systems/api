# -*- coding: utf-8 -*-
import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(str(Path(__file__).parent.joinpath('.env')))

class Config:
    """Set Flask configuration from .env file."""
    # General config
    ENV = os.environ.get('FLASK_ENV')
    DEBUG = os.environ.get('FLASK_DEBUG')

    # db conf
    MONGODB_SETTINGS = {
        'db': 'admin',
        'port': int(os.environ['MONGO_PORT']),
        'host': os.environ['MONGO_HOST'],
        'username': os.environ['MONGO_USER'],
        'password': os.environ['MONGO_PASS']
    }
    RESTX_MASK_SWAGGER = False
    # storage path config
    STORAGE_PATH = os.environ.get('STORAGE_PATH')

class TestConfig:
    """Set Flask testing environment."""
    db_fd, db_path = tempfile.mkstemp()
    # General config
    ENV = "development"
    DEBUG = True
    TESTING = True
    # db conf
    MONGO_URI="mongomock://localhost"
    RESTX_MASK_SWAGGER = False
    # storage path config
    STORAGE_PATH = db_path
