# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs."""


from elasticsearch import VERSION as ES_VERSION
from werkzeug.utils import import_string


lt_es7 = ES_VERSION[0] < 7


# FIXME: Where do we put this function, no utils please.
def obj_or_import_string(value, default=None):
    """Import string or return object.
    :params value: Import path or class object to instantiate.
    :params default: Default object to return if the import fails.
    :returns: The imported object.
    """
    if isinstance(value, str):
        return import_string(value)
    elif value:
        return value
    return default


RESOURCES_DEFAULT_VALUE = "foobar"
"""Default value for the application."""

RESOURCES_BASE_TEMPLATE = "invenio_resources/base.html"
"""Default base template for the demo page."""
