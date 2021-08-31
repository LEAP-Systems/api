# -*- coding: utf-8 -*-
"""
Models Routes
=============
Modified: 2021-07

Copyright © 2021 LEAP. All Rights Reserved.
"""

import time
import numpy as np
from typing import List, Optional
from flask.helpers import make_response
from flask.json import jsonify
from PIL import Image
from flask import request
from flask import current_app as app
from flask_restx import Resource
from mongoengine.errors import ValidationError

from app.v1.utils import fit
from app.v1.models.model import Model, api, model, post_model
from app.v1.models.capture import Capture
from app.v1.models.erosion import Erosion
from app.v1.models.dialation import Dialation
from app.v1.models.gaussian_blur import GaussianBlur
from app.v1.models.threshold import Threshold
from app.v1.models.apex import Apex
from app.v1.models.gaussian import GaussianCurve


@api.route('')
class ModelsList(Resource):

    @api.marshal_with(model, code=201)
    @api.expect(post_model, validate=True)
    def post(self):
        payload: dict = request.get_json()
        app.logger.info("Received Payload: %s", payload)
        capture_id: str = payload['capture_id']
        iterations: int = payload['iterations']
        divisor: int = payload['divisor']
        # query db for image path
        img_path = Capture.objects().get(id=capture_id).path  # type: ignore
        app.logger.debug("Recovered image path: %s", img_path)
        img = np.array(Image.open(img_path))
        processed, gaussian_blur, erosion, dialation, threshold = self.processing_pipeline(
            img, payload
        )
        app.logger.debug("Loaded image from file system. Starting processing")
        # perform gaussian curve fit
        start = time.time()
        try:
            # TODO: #10 - filter optimized gaussians by their covariance
            par, opt, cse = fit.gaussian(processed, divisor, iterations)
        except RuntimeError as exc:
            return make_response(jsonify(exc), 500)
        if par.shape != opt.shape:
            app.logger.critical("Initial and optimial parameter mismatch")
        elapsed = time.time() - start
        app.logger.debug("completed algorithm execution in %f", elapsed)
        # build apex list
        apexes: List[Apex] = []
        app.logger.debug("PAR: %s", par)
        app.logger.debug("OPT: %s", opt)
        for ax in range(par.shape[0]):
            apexes.append(
                Apex(
                    chi=cse,
                    initial=GaussianCurve(
                        amplitude=par[ax][0],
                        mu_x=par[ax][1],
                        sigma_x=par[ax][2],
                        mu_y=par[ax][3],
                        sigma_y=par[ax][4]
                    ),
                    optimized=GaussianCurve(
                        amplitude=opt[ax][0],
                        mu_x=opt[ax][1],
                        sigma_x=opt[ax][2],
                        mu_y=opt[ax][3],
                        sigma_y=opt[ax][4]
                    )
                )
            )
        app.logger.debug("Creating model")
        # create model
        model = Model(
            capture_id=capture_id,
            erosion=erosion,
            dialation=dialation,
            gaussian_blur=gaussian_blur,
            threshold=threshold,
            elapsed=elapsed,
            apexes=apexes
        )
        try:
            model.save()
        except ValidationError as exc:
            app.logger.exception("Model validation failed: %s", exc)
            return make_response(jsonify(message="Invalid types for models {}".format(exc))), 400
        app.logger.debug("Saved model")
        return model

    @staticmethod
    def processing_pipeline(img: np.ndarray, payload: dict):
        # extract optional parameters if any
        gaussian_blur_params: Optional[dict] = payload.get("gaussian_blur")
        erosion_params: Optional[dict] = payload.get("erosion")
        dialation_params: Optional[dict] = payload.get("dialation")
        threshold_params: Optional[dict] = payload.get("threshold")
        gaussian_blur = None
        threshold = None
        dialation = None
        erosion = None
        # perform some kind of processing
        if gaussian_blur_params:
            # check for these parameters in the database
            # TODO: perform check -> if None then create new
            gaussian_blur = GaussianBlur(kernel_width=5, kernel_height=5).save()
            app.logger.debug("Saved gb modifier: %s", gaussian_blur)
            # then perform the job
            # img = gaussian_blur(img, params)
        if erosion_params:
            erosion = Erosion(kernel_width=5, kernel_height=5, iterations=5).save()
            app.logger.debug("Saved erosion modifier: %s", erosion)
        if dialation_params:
            dialation = Dialation(kernel_width=5, kernel_height=5, iterations=5).save()
            app.logger.debug("Saved dialation modifier: %s", dialation)
        if threshold_params:
            threshold = Threshold(threshold=100, output=240, type="normal").save()
            app.logger.debug("Saved threshold modifier: %s", threshold)
        return img, gaussian_blur, erosion, dialation, threshold


@api.route('/<string:id>')
class Models(Resource):

    @api.marshal_with(model, code=200)
    def get(self, id: str):
        """
        Get model of a single capture 
        """
        # poll for status completion
        model = Model.objects.get(id=id)  # type: ignore
        return model
