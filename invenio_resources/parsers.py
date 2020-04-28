# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs."""

from flask_resources.args import RequestParser
from flask_resources.args.parsers import search_request_parser
from marshmallow.validate import Regexp
from webargs.fields import String


record_item_parser = RequestParser(
    fields={
        "pid_value": String(
            required=True, validation=Regexp(r"^[a-z0-9]{5}-[a-z0-9]{5}$"),
        )
    }
)

record_search_parser = search_request_parser
record_search_parser.fields.update({"q": String()})
