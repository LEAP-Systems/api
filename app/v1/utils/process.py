# -*- coding: utf-8 -*-
from app.v1.models.processor import Processor
import numpy as np
# from flask import current_app as app


class Modifiers:
    @staticmethod
    def gaussian_blur(img: np.ndarray, params: dict) -> np.ndarray: ...

    @staticmethod
    def threshold(img: np.ndarray, params: dict) -> np.ndarray: ...

    @staticmethod
    def erosion(img: np.ndarray, params: dict) -> np.ndarray: ...

    @staticmethod
    def dialation(img: np.ndarray, params: dict) -> np.ndarray: ...


def process(img: np.ndarray, processor: Processor) -> np.ndarray:
    if processor.dialation:
        img = Modifiers.dialation(img, processor.dialation)
    if processor.erosion:
        img = Modifiers.dialation(img, processor.erosion)
    if processor.threshold:
        img = Modifiers.threshold(img, processor.threshold)
    if processor.gaussian_blur:
        img = Modifiers.threshold(img, processor.gaussian_blur)
    return img
