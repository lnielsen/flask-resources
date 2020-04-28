# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs."""
import uuid

from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore import current_pidstore
from invenio_records.api import Record
from invenio_search import RecordsSearch

from .search import es_search_factory
from .config import lt_es7, obj_or_import_string


class SearchFactory:
    def create(query, ctx):

    def filters()


    def aggregations()


    def query_parser()
        #...


# TODO: Is there a generic InvenioResourceController class needed?
class RecordController:
    """Invenio record resource controller."""

    def __init__(
        self,
        pid_type_name="recid",
        pid_fetcher_name="recid",
        pid_minter_name="recid",
        record_class=Record,
        indexer_class=RecordIndexer,
        search_class=RecordsSearch,
        search_factory=SearchFactory,
    ):
        """Contructor."""
        self.pid_minter_name = pid_minter_name
        self._minter = None
        self.pid_fetcher_name = pid_fetcher_name
        self._fetcher = None
        self.pid_name = pid_type_name  # TODO: Needed?
        self.record_class = record_class
        self.indexer_class = indexer_class
        # self.search_class = search_class
        self.search_factory = SearchFactory

    def minter(self, rec_uuid, data):
        """Lazy loads the minter."""
        # Needs lazy loading. No app ctx when registering blueprint
        if not self._minter:
            self._minter = current_pidstore.minters[self.pid_minter_name]

        return self._minter(rec_uuid, data=data)

    def fetcher(self, rec_uuid):
        """Lazy loads the minter."""
        # Needs lazy loading. No app ctx when registering blueprint
        if not self._fetcher:
            self._fetcher = current_pidstore.minters[self.pid_fetcher_name]

        return self._fetcher(rec_uuid)

    @cached_property
    def resolver(self):
        return Resolver()

    @permission_required('search')
    def search(self, query=None, from_idx=None, to_idx=None, ctx=None):
        #...
        search = self.search_factory(ctx=ctx.user_needs)
        # We need a wrapper to somehow serialise back out the result. Like the marshmallow schema should be used for this.
        return SearchResult(search.execute()

    def search(self, pagination, query):
        """Perform a search over the items."""
        search_obj = self.search_class()
        search_action = search_obj.with_preference_param().params(version=True)
        search_action = search_action[
            pagination["from_idx"] : pagination["to_idx"]
        ]
        if not lt_es7:
            search_action = search_action.extra(track_total_hits=True)

        # Lars: Can we avoid this extra factory?
        search_action = self.search_factory(
            search=search_action, query_string=query
        )

        # Execute search
        # Lars: we need to return a proper representation
        return search_action.execute()

    @permission_required('search')
    def create(self, data, index=True, ctx=None):
        """Create a record."""
        # Lars: We need a marshmallow schema here that does business logic data validation.
        # - this schema should be used for both records and deposits.
        data = self.schema_cls().load(data)

        # Create uuid for record
        record_uuid = uuid.uuid4()
        # Create persistent identifier
        # Lars: in schema or outside schema.
        pid = self.minter(record_uuid, data=data)
        # Create record
        record = self.record_class.create(data, id_=record_uuid)

        db.session.commit()

        # Index the record
        if self.indexer_class:
            self.indexer_class().index(record)

        return record

    @resolve('id')
    @permission_required('read')
    def read(self, pid, record):
        """Read an item."""
        # TODO
        return None

    def delete(self, rec_uuid):
        """Delete an item."""
        return {"status": "Accepted"}

## usage
ctrl = RecordController()
record  = ctrl.create(
    dict(title=..)
    ctx={user_needs=current_identity.provies}
)

ctx = dict(needs='current_identity.provides')
record = ctrl.read('axcfd-acdf', ctx=ctx)
record.data['title'] = 'test'
ctrl.update(record)

record = ctrl.create(Record(data={})) #???

