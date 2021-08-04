# -*- coding: utf-8 -*-
"""
Models Routes
=============
Modified: 2021-07

Copyright © 2021 LEAP. All Rights Reserved.
"""

import time
from typing import List
import numpy as np
from flask.helpers import make_response
from flask.json import jsonify
from mongoengine.errors import ValidationError
from PIL import Image
from flask import current_app as app
from flask_restx import Resource
from app.v1.functions import fit
from app.v1.models.model import Model
from app.v1.models.capture import Capture
from app.v1.models.processing import Erosion, Dialation, GaussianBlur, Threshold
from app.v1.models.apex import Apex, GaussianCurve
from app.v1.namespaces.model import api, model_model, post_model


@api.route('')
class ModelsList(Resource):

    @api.marshal_with(model_model, code=201)
    @api.expect(post_model, validate=True)
    def post(self):
        args = post_model.parse_args(strict=True)
        divisor: int = args["divisor"]
        capture_id: str = args["capture_id"]
        iterations: int = args["iterations"]
        # query db for image path
        img_path = Capture.objects().get(id=capture_id).path  # type: ignore
        img = np.array(Image.open(img_path))
        # perform some kind of processing
        gb = GaussianBlur(kernel_width=5, kernel_height=5)
        erosion = Erosion(kernel_width=5, kernel_height=5, iterations=5)
        dialation = Dialation(kernel_width=5, kernel_height=5, iterations=5)
        threshold = Threshold(threshold=100, output=240, type="normal")
        # perform gaussian curve fit
        start = time.time()
        try:
            # TODO: #10 - filter optimized gaussians by their covariance
            par, opt, _, cse = fit.gaussian(img, divisor, iterations)
        except RuntimeError as exc:
            return make_response(jsonify(exc), 500)
        if par.shape != opt.shape:
            app.logger.critical("Initial and optimial parameter mismatch")
        elapsed = time.time() - start
        # build apex list
        apexes: List[Apex] = []
        for ax in range(par.shape[0]):
            apexes.append(
                Apex(
                    guess=GaussianCurve(
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
        model = Model(
            capture_id=capture_id,
            erosion=erosion,
            dialation=dialation,
            gaussian_blur=gb,
            threshold=threshold,
            chi_squared_error=cse,
            elapsed=elapsed,
            apexes=apexes
        )
        try:
            model.save()
        except ValidationError as exc:
            app.logger.exception("Model validation failed: %s", exc)
            return make_response(jsonify(message="Invalid types for models {}".format(exc))), 400
        return model


@api.route('/<string:id>')
class Models(Resource):

    # @api.marshal_with(capture_marshal, code=200)
    def get(self, id: str):
        """
        Get model of a single capture 
        """
        # poll for status completion
        model = Model.objects.get(capture_id=id)  # type: ignore
        return model
