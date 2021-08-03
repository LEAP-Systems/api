# -*- coding: utf-8 -*-
import mongoengine as me


class GaussianCurve(me.EmbeddedDocument):
    amplitude = me.FloatField()
    sigma_x = me.FloatField()
    sigma_y = me.FloatField()
    mu_x = me.IntField()
    mu_y = me.IntField()


class Apex(me.EmbeddedDocument):
    initial = me.EmbeddedDocumentField(GaussianCurve)
    optimized = me.EmbeddedDocumentField(GaussianCurve)
