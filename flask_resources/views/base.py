# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Flask Resources module to create REST APIs.

The views responsabilities are:
- Parse request arguments.
- Build a request context for the resource.
"""

from flask.views import MethodView

from ..content_negotiation import content_negotiation
from ..context import with_resource_requestctx


class BaseView(MethodView):
    """Base view."""

    resource_decorators = [content_negotiation, with_resource_requestctx]
    """Resource-specific decorators to be applied to the views."""
    # todo: can https://flask.palletsprojects.com/en/1.1.x/api/#flask.views.View.decorators
    # be used instead?

    def __init__(self, resource, *args, **kwargs):
        """Constructor."""
        super(BaseView, self).__init__(*args, **kwargs)
        self.resource = resource

    def dispatch_request(self, *args, **kwargs):
        """Dispatch request after applying resource decorators."""
        view = MethodView.dispatch_request

        for decorator in self.resource_decorators:
            view = decorator(view)

        return view(self, *args, **kwargs)
