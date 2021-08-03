# -*- coding: utf-8 -*-
import numpy as np
from typing import List, Tuple, Union
from flask import current_app as app
from scipy import optimize


def gauss(data: np.ndarray,
          a0: int, mu_x0: int, sig_x0: float, mu_y0: int, sig_y0: float,
          a1: int, mu_x1: int, sig_x1: float, mu_y1: int, sig_y1: float,
          a2: int, mu_x2: int, sig_x2: float, mu_y2: int, sig_y2: float,
          a3: int, mu_x3: int, sig_x3: float, mu_y3: int, sig_y3: float,
          a4: int, mu_x4: int, sig_x4: float, mu_y4: int, sig_y4: float,
          a5: int, mu_x5: int, sig_x5: float, mu_y5: int, sig_y5: float,
          a6: int, mu_x6: int, sig_x6: float, mu_y6: int, sig_y6: float,
          a7: int, mu_x7: int, sig_x7: float, mu_y7: int, sig_y7: float) -> np.ndarray:
    x = data[0, :, :]
    y = data[1, :, :]
    res = a0 * np.exp(-((x - mu_x0)**2 / (2 * sig_x0**2) + (y - mu_y0)**2 / (2 * sig_y0**2))) + \
        a1 * np.exp(-((x - mu_x1)**2 / (2 * sig_x1**2) + (y - mu_y1)**2 / (2 * sig_y1**2))) + \
        a2 * np.exp(-((x - mu_x2)**2 / (2 * sig_x2**2) + (y - mu_y2)**2 / (2 * sig_y2**2))) + \
        a3 * np.exp(-((x - mu_x3)**2 / (2 * sig_x3**2) + (y - mu_y3)**2 / (2 * sig_y3**2))) + \
        a4 * np.exp(-((x - mu_x4)**2 / (2 * sig_x4**2) + (y - mu_y4)**2 / (2 * sig_y4**2))) + \
        a5 * np.exp(-((x - mu_x5)**2 / (2 * sig_x5**2) + (y - mu_y5)**2 / (2 * sig_y5**2))) + \
        a6 * np.exp(-((x - mu_x6)**2 / (2 * sig_x6**2) + (y - mu_y6)**2 / (2 * sig_y6**2))) + \
        a7 * np.exp(-((x - mu_x7)**2 / (2 * sig_x7**2) + (y - mu_y7)**2 / (2 * sig_y7**2)))
    return np.ravel(res)


def generate_par(width: int, height: int) -> np.ndarray:
    return np.array([
        [250, width / 5, width * 0.05, height / 5, height * 0.05],
        [250, width / 5, width * 0.05, height - height / 5, height * 0.05],
        [200, width / 3, width * 0.03, height / 3, height * 0.03],
        [200, width / 3, width * 0.03, height - height / 3, height * 0.03],
        [250, width - width / 5, width * 0.05, height / 5, height * 0.05],
        [250, width - width / 5, width * 0.05, height - height / 5, height * 0.05],
        [200, width - width / 3, width * 0.03, height / 3, height * 0.03],
        [200, width - width / 3, width * 0.03, height - height / 3, height * 0.03],
    ]).flatten()


def gaussian(img: np.ndarray, res: int, iterations: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    app.logger.debug("Computing multi gaussian fit @ 1/%s resolution", res)
    # normalize minimum pixel values (flatten noise floor)
    img -= np.min(img)
    # quarter res
    _input = img[::res, ::res]
    width, height = _input.shape
    _input = np.ravel(_input)
    # create axis points and populate all points on grid
    x, y = np.linspace(0, width, width), np.linspace(0, height, height)
    X, Y = np.meshgrid(x, y)
    x_data = []
    x_data.append(X)
    x_data.append(Y)
    x_data = np.array(x_data)
    # set mu_x, mu_y guesses as a function of the image size
    par = generate_par(width, height)
    app.logger.info("Executing curve fit with initial parameters: %s", par)
    # 2D Gaussian fit
    popt, pcov = optimize.curve_fit(gauss, x_data, _input, p0=par,  # type: ignore
                                    maxfev=iterations)
    app.logger.info("Optimized: %s", popt)
    app.logger.info("Covariance: %s", pcov)
    model = gauss(_input, *par)
    # apply chi squared minimization
    chi = np.subtract(_input, model)**2 / model
    cse = np.mean(chi)
    return par, popt, pcov, cse
