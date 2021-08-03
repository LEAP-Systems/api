# -*- coding: utf-8 -*-
import mongoengine as me


class GaussianBlur(me.EmbeddedDocument):
    kernel_width = me.IntField(required=True)
    kernel_height = me.IntField(required=True)


class Erosion(me.EmbeddedDocument):
    kernel_width = me.IntField(required=True)
    kernel_height = me.IntField(required=True)
    iterations = me.IntField(required=True)


class Dialation(me.EmbeddedDocument):
    kernel_width = me.IntField(required=True)
    kernel_height = me.IntField(required=True)
    iterations = me.IntField(required=True)


class Threshold(me.EmbeddedDocument):
    threshold = me.IntField(required=True)
    output = me.IntField(required=True)
    type = me.StringField(required=True)
