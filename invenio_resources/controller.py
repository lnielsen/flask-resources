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
        search_factory=es_search_factory,
    ):
        """Contructor."""
        self.pid_minter_name = pid_minter_name
        self._minter = None
        self.pid_fetcher_name = pid_fetcher_name
        self._fetcher = None
        self.pid_name = pid_type_name  # TODO: Needed?
        self.record_class = record_class
        self.indexer_class = indexer_class
        self.search_class = search_class
        self.search_factory = obj_or_import_string(search_factory)

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

    def search(self, pagination, query):
        """Perform a search over the items."""
        search_obj = self.search_class()
        search_action = search_obj.with_preference_param().params(version=True)
        search_action = search_action[
            pagination["from_idx"] : pagination["to_idx"]
        ]
        if not lt_es7:
            search_action = search_action.extra(track_total_hits=True)

        search_action = self.search_factory(
            search=search_action, query_string=query
        )

        # Execute search
        return search_action.execute()

    def create(self, data):
        """Create a record."""
        # Create uuid for record
        record_uuid = uuid.uuid4()
        # Create persistent identifier
        pid = self.minter(record_uuid, data=data)
        # Create record
        record = self.record_class.create(data, id_=record_uuid)

        db.session.commit()

        # Index the record
        if self.indexer_class:
            self.indexer_class().index(record)

        return record

    def read(self, rec_uuid):
        """Read an item."""
        # TODO
        return None

    def delete(self, rec_uuid):
        """Delete an item."""
        return {"status": "Accepted"}
