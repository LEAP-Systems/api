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
    def dilation(img: np.ndarray, params: dict) -> np.ndarray: ...


def process(img: np.ndarray, processor: Processor) -> np.ndarray:
    if processor.dilation:
        img = Modifiers.dilation(img, processor.dilation)
    if processor.erosion:
        img = Modifiers.dilation(img, processor.erosion)
    if processor.threshold:
        img = Modifiers.threshold(img, processor.threshold)
    if processor.gaussian_blur:
        img = Modifiers.threshold(img, processor.gaussian_blur)
    return img
