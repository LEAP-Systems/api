#!/opt/homebrew/bin/python3
import logging
import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt
from PIL import Image
import time

_log = logging.getLogger(__name__)


def super_gauss(data, a0, mu_x0, sig_x0, mu_y0, sig_y0, a1, mu_x1, sig_x1, mu_y1, sig_y1,
                a2, mu_x2, sig_x2, mu_y2, sig_y2, a3, mu_x3, sig_x3, mu_y3, sig_y3, a4, mu_x4, sig_x4, mu_y4, sig_y4,
                a5, mu_x5, sig_x5, mu_y5, sig_y5, a6, mu_x6, sig_x6, mu_y6, sig_y6, a7, mu_x7, sig_x7, mu_y7, sig_y7):
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


def plot(title: str, data: np.ndarray, out_path: str):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    cmap = ax.imshow(data, origin='upper', vmin=0, vmax=255)
    plt.colorbar(cmap)
    plt.savefig(out_path)
    _log.debug("Saved %s", out_path)


def gaussian_fit(img_path: str, res: int, iterations: int):
    _log.debug("Computing multi gaussian fit @ 1/%s resolution", res)
    _input = np.array(Image.open(img_path))
    # normalize minimum pixel values (flatten noise floor)
    _input -= np.min(_input)
    # quarter res
    _input = _input[::res, ::res]
    width, height = _input.shape
    _input = np.ravel(_input)

    # create axis points and populate all points on grid
    x = np.linspace(0, width, width)
    y = np.linspace(0, height, height)
    X, Y = np.meshgrid(x, y)
    x_data = []
    x_data.append(X)
    x_data.append(Y)
    x_data = np.array(x_data)
    # set mu_x, mu_y guesses as a function of the image size
    par = [
        [250, width / 5, 10, height / 5, 10],
        [250, width / 5, 10, height - height / 5, 10],
        [200, width / 3, 7, height / 3, 7],
        [200, width / 3, 7, height - height / 3, 7],
        [250, width - width / 5, 10, height / 5, 10],
        [250, width - width / 5, 10, height - height / 5, 10],
        [200, width - width / 3, 7, height / 3, 7],
        [200, width - width / 3, 7, height - height / 3, 7],
    ]
    par = np.array(par).flatten()
    model = super_gauss(x_data, *par)
    plot('Initial Gaussian Distributions', np.reshape(model, newshape=(width, height)), 'output/guess.png')
    plot('Capture', np.reshape(_input, newshape=(width, height)), 'output/input.png')
    _log.info("Executing curve fit with initial parameters: %s", par)
    # 2D Gaussian fit
    start = time.time()
    popt, pcov = optimize.curve_fit(super_gauss, x_data, _input, p0=par, maxfev=iterations)
    _log.info("Curve fit elapsed time: %s", time.time() - start)
    _log.info("Optimized: %s", popt)
    _log.info("Covariance: %s", pcov)

    # plot optimized
    model = super_gauss(x_data, *popt)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('Optimized Gaussian Distributions')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    cmap = ax.imshow(np.reshape(model, newshape=(width, height)),
                     origin='upper', vmin=0, vmax=255)
    popt = [round(x, 2) for x in popt]
    plt.colorbar(cmap)
    popt = np.array(popt)
    popt = np.reshape(popt, newshape=(8, 5))
    for params in popt:
        ax.annotate(f'a={params[0]}\nσx={params[2]}\nσy={params[4]}', (params[1], params[3]))
        ax.plot(params[1], params[3], marker='+')
    plt.savefig('output/optimized.png')
    # diff = (model - _input)**2
