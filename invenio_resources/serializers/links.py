# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs."""

from flask import url_for
from flask_resources.resources import ITEM_VIEW_SUFFIX


def record_link(record, endpoint):

    endpoint = ".{}{}".format(endpoint, ITEM_VIEW_SUFFIX)
    if not isinstance(record, dict):
        record = record.dumps()

    # TODO Config with Persisten identifier attribute name from config
    return url_for(endpoint, pid_value=record["recid"], _external=True)


def default_links_factory(record, endpoint, *args, **kwargs):
    """Factory for record links generation.
    :returns: Dictionary containing a list of useful links for the record.
    """

    return {"self": record_link(record, endpoint)}
