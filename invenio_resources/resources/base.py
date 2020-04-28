# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs."""

from flask import abort
from flask_resources.context import resource_requestctx
from functools import wraps

from ..config import obj_or_import_string
from ..errors import InvalidDataRESTError, UnsupportedMediaRESTError


def content_negotiation(f):
    @wraps(f)
    def inner(self, *args, **kwargs):
        # resource_requestctx.payload_mimetype = ContentNegotiator.match(
        #     self.item_loaders.keys(),
        #     request.content_type,
        #     {},  # self.formats,
        #     request.args.get("format", None),
        #     None,  # self.default_mimetype,
        # )

        # FIXME: content negotiation
        payload_mimetype = "application/json"  # Content-Type
        accept_mimetype = "application/json"

        # Check if content-type can be treated otherwise, fail fast
        # Serialization is checked per function due to lack of
        # knowledge at this point
        if payload_mimetype not in self.config.item_loaders.keys():
            raise UnsupportedMediaRESTError(payload_mimetype)

        resource_requestctx.payload_mimetype = payload_mimetype
        resource_requestctx.accept_mimetype = accept_mimetype

        return f(self, *args, **kwargs)

    return inner


def load_request(f):
    @wraps(f)
    def inner(self, *args, **kwargs):
        if resource_requestctx.payload_mimetype is None:
            abort(406)

        data = self.load_item_from_request(
            content_type=resource_requestctx.payload_mimetype
        )
        if data is None:
            raise InvalidDataRESTError()

        return f(self, data=data, *args, **kwargs)

    return inner


class InvenioResourceConfig(object):
    """Resource configuration."""

    def __init__(
        self,
        list_serializers=None,
        item_serializers=None,
        item_loaders=None,
        list_route=None,
        item_route=None,
    ):
        """Constructor."""
        self.item_loaders = {
            mime: obj_or_import_string(func)
            for mime, func in item_loaders.items()
        }
        self.item_serializers = {
            mime: obj_or_import_string(func)
            for mime, func in item_serializers.items()
        }
        self.list_serializers = {
            mime: obj_or_import_string(func)
            for mime, func in list_serializers.items()
        }
        self.list_route = list_route
        self.item_route = item_route
