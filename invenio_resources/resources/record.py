# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs."""

from flask import make_response
from flask_resources import CollectionResource
from flask_resources.context import resource_requestctx
from flask_resources.args.parsers import create_request_parser
from functools import partial

from ..config import lt_es7
from ..controller import RecordController
from ..errors import UnsupportedMediaRESTError
from ..loaders import default_record_loaders
from ..parsers import record_item_parser, record_search_parser
from ..serializers import (
    default_record_item_serializers,
    default_record_list_serializers,
)
from .base import InvenioResourceConfig, load_request, content_negotiation
from ..serializers.links import default_links_factory, record_link


class RecordResourceConfig(InvenioResourceConfig):
    """Record resource config."""

    def __init__(
        self,
        item_route="/records/<pid_value>",
        list_route="/records",
        list_serializers=default_record_list_serializers,
        item_serializers=default_record_item_serializers,
        item_loaders=default_record_loaders,
        links_factory=default_links_factory,
        *args,
        **kwargs
    ):
        """Constructor."""
        super(RecordResourceConfig, self).__init__(
            item_route=item_route,
            list_route=list_route,
            list_serializers=list_serializers,
            item_serializers=item_serializers,
            item_loaders=item_loaders,
            *args,
            **kwargs
        )
        self.links_factory = links_factory
        self.create_request_parser = kwargs.get(
            "record_search_parser", create_request_parser
        )
        self.item_request_parser = kwargs.get(
            "record_item_parser", record_item_parser
        )
        self.search_request_parser = kwargs.get(
            "record_create_parser", record_search_parser
        )


# FIXME: Sort and faceting??
class RecordResource(CollectionResource):
    """Record resource."""

    def __init__(
        self,
        config=RecordResourceConfig(),
        controller=RecordController(),
        *args,
        **kwargs
    ):
        """Constructor."""
        super(RecordResource, self).__init__(
            config=config, controller=controller, *args, **kwargs
        )

    #
    # Primary Interface
    #

    @content_negotiation
    def search(self):
        """Perform a search over the items."""
        # Check if accept-type can be treated otherwise, fail fast
        accept_mimetype = resource_requestctx.accept_mimetype
        if accept_mimetype not in self.config.list_serializers.keys():
            raise UnsupportedMediaRESTError(accept_mimetype)

        # Controller searches record
        try:
            return self.make_list_response(
                self.controller.search(
                    pagination=resource_requestctx.request_args.get(
                        "pagination", None
                    ),
                    query=resource_requestctx.request_args.get("q", ""),
                ),
                200,
            )
        # FIXME: What type of errors can occur
        except:
            return self.make_error_response(None, 500)

    @content_negotiation
    @load_request
    def create(self, data):
        """Create an item."""
        # Request loading happens in the decorator
        # Check if accept-type can be treated otherwise, fail fast
        accept_mimetype = resource_requestctx.accept_mimetype
        if accept_mimetype not in self.config.item_serializers.keys():
            raise UnsupportedMediaRESTError(accept_mimetype)

        # Controller creates record
        try:
            return self.make_item_response(self.controller.create(data), 200)
        # FIXME: What type of errors can occur
        except:
            return self.make_error_response(data, 500)

    def read(self):
        """Read an item."""
        # return make_response(self.resource.read(request_context), 200)
        # rec_uuid = resourcerequest_ctx.request_args.get("pid_value")
        # return self.controller.read(rec_uuid, ctx={user=current_user})
        pass

    def update(self):
        """Update an item."""
        # Data goes in the context
        # return make_response(self.resource.update(request_context), 200)
        # rec_uuid = resourcerequest_ctx.request_args.get("pid_value")
        # return self.controller.update(rec_uuid)
        pass

    def partial_update(self):
        """Patch an item."""
        # return make_response(self.resource.patch(request_context), 200)
        # rec_uuid = request_context.request_args.get("pid_value")
        # return self.controller.patch(rec_uuid)
        pass

    def delete(self):
        """Delete an item."""
        # make_response(self.resource.delete(request_context), 204)
        # rec_uuid = request_context.request_args.get("pid_value")
        # return self.controller.delete(rec_uuid)
        pass

    #
    # Secondary Interface
    #
    def load_item_from_request(self, content_type):
        try:
            return self.config.item_loaders[content_type]()
        except KeyError:
            raise UnsupportedMediaRESTError(content_type)

    def make_list_response(self, search_result, http_code):

        total = (
            search_result.hits.total
            if lt_es7
            else search_result.hits.total["value"]
        )

        link_from_record = partial(
            self.config.links_factory, endpoint=self.bp_name
        )

        response_ctx = {
            "links": link_from_record,
            "prettyprint": resource_requestctx.request_args.get(
                "prettyprint", False
            ),
        }
        serialized_search_result = self.config.list_serializers[
            resource_requestctx.accept_mimetype
        ].serialize_search(total, search_result.to_dict(), response_ctx)

        # # Generate links for self/prev/next

        # endpoint = get_view_name(self.name, LIST_VIEW)
        # location = url_for(".{}".format(endpoint), _external=True)

        # FIXME: pagination
        # urlkwargs.update(size=pagination["size"], _external=True)

        # links = {}

        # def _link(name):
        #     urlkwargs.update(pagination["links"][name])
        #     links[name] = url_for(endpoint, **urlkwargs)

        # _link("self")
        # if pagination["from_idx"] >= 1:
        #     _link("prev")
        # if pagination["to_idx"] < min(total, self.max_result_window):
        #     _link("next")

        response = make_response(serialized_search_result, 200)

        # Add location headers
        # TODO

        return response

    # FIXME: The interface is `item` but `record` looks better here
    def make_item_response(self, record, http_code):

        link_from_record = partial(
            self.config.links_factory, endpoint=self.bp_name
        )

        response_ctx = {
            "links": link_from_record,
            "prettyprint": resource_requestctx.request_args.get(
                "prettyprint", False
            ),
        }
        serialized_item = self.config.item_serializers[
            resource_requestctx.accept_mimetype
        ].serialize(record, response_ctx)

        response = make_response(serialized_item, 201)

        # Add location headers
        response.headers.extend(
            {"location": record_link(record, self.bp_name)}
        )

        return response

    def make_error_response(self, item, http_code):
        # self.config.error_I serializer()
        #     try:
        #         return self.list_serializers[content_type](item_list)
        #     except KeyError:
        #         raise UnsupportedMediaRESTError(content_type)

        pass
