# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resource Request context."""

from functools import wraps

from flask import g
from werkzeug.local import LocalProxy


#
# Proxy to the current resource context
#
def _get_context():
    """Get the resource request context from the g object."""
    if hasattr(g, "resource_requestctx"):
        return g.resource_requestctx
    raise RuntimeError("Working outside of resource request context.")


resource_requestctx = LocalProxy(_get_context)
"""Proxy to the resource's request context"""


#
# Resource context
#
class ResourceRequestCtx(object):
    """Context manager for the resource context.

    The resource request context encodes information about the currently
    executing request for a given resource, such as:

    - The mimetype selected by the content negotiation.
    - The content type of the request payload
    """

    def __init__(
        self, accept_mimetype=None, payload_mimetype=None, request_args=None, data=None,
    ):
        """Initialize the resource context."""
        self.accept_mimetype = accept_mimetype
        self.payload_mimetype = payload_mimetype  # Content-Type
        self.request_args = request_args
        self.data = data

    def __enter__(self):
        """Push the resource context manager on the current request."""
        g.resource_requestctx = self

    def __exit__(self, type, value, traceback):
        """Pop the resource context manager from the current request."""
        del g.resource_requestctx


def with_resource_requestctx(f):
    """Wrap in resource request context."""

    @wraps(f)
    def inner(*args, **kwargs):
        with ResourceRequestCtx():
            return f(*args, **kwargs)

    return inner
