# -*- coding: utf-8 -*-
import mongoengine as me

class GaussCurve(me.EmbeddedDocument):
    amplitude = me.FloatField()
    sigma_x = me.FloatField()
    sigma_y = me.FloatField()
    mu_x = me.IntField()
    mu_y = me.IntField()
