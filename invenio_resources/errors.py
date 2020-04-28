# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs."""

from invenio_rest.errors import RESTException

# TODO: Revise this

#
# Query
#
class InvalidQueryRESTError(RESTException):
    """Invalid query syntax."""

    code = 400
    description = "Invalid query syntax."


#
# Loading/Serializing
#
class UnsupportedMediaRESTError(RESTException):
    """Creating record with unsupported media type."""

    code = 415

    def __init__(self, content_type=None, **kwargs):
        """Initialize exception."""
        super(UnsupportedMediaRESTError, self).__init__(**kwargs)
        content_type = content_type
        self.description = 'Unsupported media type "{0}".'.format(content_type)


class InvalidDataRESTError(RESTException):
    """Invalid request body."""

    code = 400
    description = "Could not load data."
