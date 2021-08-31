# -*- coding: utf-8 -*-
"""
Testing Config
==============
Modified: 2021-08

Copyright © 2021 LEAP. All Rights Reserved.
"""

import pytest
from app import init_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = init_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!
