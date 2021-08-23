# -*- coding: utf-8 -*-
import numpy as np
from flask import current_app as app
from typing import Tuple
from app.v1.models.erosion import Erosion
from app.v1.models.dialation import Dialation
from app.v1.models.gaussian_blur import GaussianBlur
from app.v1.models.threshold import Threshold


class Modifiers:
    @staticmethod
    def gaussian_blur(img: np.ndarray, params: dict) -> Tuple[np.ndarray, GaussianBlur]: ...

    @staticmethod
    def threshold(img: np.ndarray, params: dict) -> Tuple[np.ndarray, Threshold]:
        threshold = Threshold(threshold=100, output=240, type="normal").save()
        app.logger.debug("Saved threshold modifier: %s", threshold)
        return img, threshold

    @staticmethod
    def erosion(img: np.ndarray, params: dict) -> Tuple[np.ndarray, Erosion]: ...

    @staticmethod
    def dialation(img: np.ndarray, params: dict) -> Tuple[np.ndarray, Dialation]: ...
