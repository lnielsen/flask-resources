# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs."""


from elasticsearch_dsl.query import Q
from flask import current_app

from ..errors import InvalidQueryRESTError


def _default_parser(qstr=None):
    """Default parser that uses the Q() from elasticsearch_dsl."""
    if qstr:
        return Q("query_string", query=qstr)
    return Q()


def default_search_factory(
    search, query_string="", query_parser=_default_parser
):
    """Parse query using elasticsearch DSL query.

    :param search: Elastic search DSL search instance.
    :param query_string: Query string
    :param query_parser: Custom query parser.
    :returns: Tuple with search instance and URL arguments.
    """

    try:
        search = search.query(query_parser(query_string))
    except SyntaxError:
        current_app.logger.debug(
            "Failed parsing query: {0}".format(query_string), exc_info=True,
        )
        raise InvalidQueryRESTError()

    return search
