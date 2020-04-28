# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs."""

from ..schemas import RecordSchemaJSONV1
from .record import JSONRercordSerializer

json_v1 = JSONRercordSerializer(RecordSchemaJSONV1)
"""JSON v1 serializer."""

# TODO: Remove if unused
# json_v1_response = record_responsify(json_v1, "application/json")
# """JSON response builder that uses the JSON v1 serializer."""

# json_v1_search = search_responsify(json_v1, "application/json")
# """JSON search response builder that uses the JSON v1 serializer."""

default_record_list_serializers = {"application/json": json_v1}
"""Default records list (search) serializer."""

default_record_item_serializers = {"application/json": json_v1}
"""Default record serializer."""
