# -*- coding: utf-8 -*-
"""
Processor Model Unittests
=========================
Modified: 2021-08

Copyright © 2021 LEAP. All Rights Reserved.
"""

import pytest
from app.v1.models.processor import Processor
from tests import resources


@pytest.fixture(scope='function')
def new_processor():
    processor = Processor(**resources.PROCESSOR_PAYLOAD)
    return processor


def test_processor(new_processor: Processor):
    assert new_processor.dilation is not None
    assert new_processor.erosion is not None
    assert new_processor.gaussian_blur is not None
    assert new_processor.threshold is not None
