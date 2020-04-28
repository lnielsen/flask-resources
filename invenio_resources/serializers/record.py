# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Record Serializer."""

import copy
import json
import pytz

from ..schemas import RecordSchemaJSONV1


class SerializerMixinInterface:
    """Serializer Interface."""

    def process_metadata(self, record, response_ctx, *args, **kwargs):
        """Process the record metadata.

        It allows to perform operations in the record metadata before. 

        :param record: Record instance.
        :param response_ctx: ctx of the response.
        :return: The record processed metadata.
        """
        raise NotImplementedError()

    def process_record(self, record, response_ctx, *args, **kwargs):
        """Process a record.

        It allows to perform operations in the record before
        it is serialized. 

        :param record: Record instance.
        :param response_ctx: ctx of the response.
        :return: The record processed metadata.
        """
        raise NotImplementedError()

    def serialize(self, record_response, response_ctx, *args, **kwargs):
        """Serialize a single record reponse according to the response ctx."""
        raise NotImplementedError()

    def process_search_hit(self, record_hit, response_ctx, *args, **kwargs):
        """Process a record hit from Elasticsearch for serialization."""
        raise NotImplementedError()

    def serialize_search(
        self, total, search_result, response_ctx, *args, **kwargs
    ):
        raise NotImplementedError()


class JSONRercordSerializer(SerializerMixinInterface):
    """Mixin serializing records as JSON."""

    def __init__(
        self, schema_class=RecordSchemaJSONV1, replace_refs=False, **kwargs
    ):
        """Initialize record."""
        super(JSONRercordSerializer, self).__init__(**kwargs)
        self.schema_class = schema_class
        self.replace_refs = replace_refs

    @staticmethod
    def _format_args(prettyprint=False):
        """Get JSON dump indentation and separates."""
        if prettyprint:
            return dict(indent=2, separators=(", ", ": "),)
        else:
            return dict(indent=None, separators=(",", ":"),)

    def dump(self, obj, ctx=None):
        """Serialize object with schema."""

        return self.schema_class(context=ctx).dump(obj).data

    def process_metadata(self, record, response_ctx, *args, **kwargs):
        return (
            copy.deepcopy(record.replace_refs())
            if self.replace_refs
            else record.dumps()
        )

    def process_record(self, record, response_ctx, *args, **kwargs):
        # TODO: Check does revision go into the Schema when dumping?
        record_dict = dict(
            pid=record.id,  # FIXME: Record contains only str id
            metadata=self.process_metadata(record, response_ctx),
            links=response_ctx.get("links")(record=record),
            revision=record.revision_id,
            created=(
                pytz.utc.localize(record.created).isoformat()
                if record.created
                else None
            ),
            updated=(
                pytz.utc.localize(record.updated).isoformat()
                if record.updated
                else None
            ),
        )

        return self.dump(record_dict)

    def serialize(self, record, response_ctx, *args, **kwargs):
        return json.dumps(
            self.process_record(record, response_ctx),
            **self._format_args(response_ctx.get("prettyprint", False))
        )

    def preprocess_search_hit(self, record_hit, response_ctx, *args, **kwargs):
        """Prepare a record hit from Elasticsearch for serialization."""
        metadata = record_hit["_source"]

        record = dict(
            # FIXME: use PID attribute name from config
            pid=metadata["recid"],
            metadata=metadata,
            links=response_ctx.get("links")(record=metadata),
            revision=record_hit["_version"],
            created=None,
            updated=None,
        )
        # Move created/updated attrs from source to object.
        for key in ["_created", "_updated"]:
            if key in record["metadata"]:
                record[key[1:]] = record["metadata"][key]
                del record["metadata"][key]

        return self.dump(record)

    def serialize_search(
        self, total, search_result, response_ctx, *args, **kwargs
    ):
        return json.dumps(
            dict(
                hits=dict(
                    hits=[
                        # FIXME: links per record
                        self.preprocess_search_hit(
                            record_hit=hit, response_ctx=response_ctx
                        )
                        for hit in search_result["hits"]["hits"]
                    ],
                    total=total,
                ),
                # TODO FIX global links
                links="",
                aggregations=search_result.get("aggregations", dict()),
            ),
            **self._format_args(response_ctx.get("prettyprint", False))
        )
