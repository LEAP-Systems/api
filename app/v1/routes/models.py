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
            processor_id=processor_id,
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
