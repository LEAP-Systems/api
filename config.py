# -*- coding: utf-8 -*-
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(str(Path(__file__).parent.joinpath('.env')))


class Config:
    """Set Flask configuration from .env file."""
    # General config
    ENV = os.environ.get('FLASK_ENV')
    DEBUG = os.environ.get('FLASK_DEBUG')

    # db conf
    MONGO_URI = os.environ.get('MONGO_URI')
