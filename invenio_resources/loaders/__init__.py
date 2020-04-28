# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs."""

# FIXME: loader should receive data and "load" it?
from flask import request

from ..schemas import RecordMetadataSchemaJSONV1, RecordSchemaJSONV1
from .marshmallow import json_patch_loader, marshmallow_loader

json_v1 = marshmallow_loader(RecordSchemaJSONV1)
"""Simple example loader that will take any JSON."""

json_patch_v1 = json_patch_loader
"""Simple example loader that will take any JSON patch."""

json_pid_checker = marshmallow_loader(RecordMetadataSchemaJSONV1)
"""Loader that will make sure the PID of the URL matches the data PID."""

default_record_loaders = {
    "application/json": lambda: request.get_json(),
    "application/json-patch+json": lambda: request.get_json(force=True),
}
