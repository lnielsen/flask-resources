# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs"""


def test_create_record(base_client):
    """Test record creation."""

    # Create draft
    draft = base_client.post("/records")
    assert draft.status_code == 201  # Draft created

    # Get draft id
    rec_uuid = draft.json.get("id", None)
    assert rec_uuid is not None

    # Update with draft content
    draft_content = draft.json.get("metadata")

    # TODO: Add some new metadata
    draft = base_client.put(
        "/records/{}/draft".format(rec_uuid), data=draft_content
    )
    assert draft.status_code == 200

    # TODO: Add case where validation fails

    draft_file = base_client.put(
        "/records/{}/draft/files/test.jpg".format(rec_uuid)
    )
    assert draft_file.status_code == 200

    # Publish record
    action = base_client.post(
        "/records/{}/draft/actions/publish".format(rec_uuid)
    )
    # Accept publishing. Might lunch async tasks.
    # TODO Should be 202
    assert action.status_code == 201

    # Get published record
    record = base_client.get("/records/{}".format(rec_uuid))
    assert record.status_code == 200
    assert record.json.get("id") == rec_uuid


def test_edit_record(base_client):
    """Test editing an existing record (new revision)."""

    # Create draft
    draft = base_client.post("/records/{}/draft".format("a1b2c-3d4e5"))
    assert draft.status_code == 201  # Draft created

    # Get draft id
    rec_uuid = draft.json.get("id", None)
    assert rec_uuid == "a1b2c-3d4e5"

    # Update with draft content
    draft_content = draft.json.get("metadata")
    # TODO: Add some new metadata
    draft = base_client.put(
        "/records/{}/draft".format(rec_uuid), data=draft_content
    )
    assert draft.status_code == 200

    # Publish record
    action = base_client.post(
        "/records/{}/draft/actions/publish".format(rec_uuid)
    )
    # Accept publishing. Might lunch async tasks.
    # TODO Should be 202
    assert action.status_code == 201

    # Get published record
    record = base_client.get("/records/{}".format(rec_uuid))
    assert record.status_code == 200
    assert record.json.get("id") == rec_uuid


def test_create_new_version(base_client):
    """Test creation of a new version of a record."""

    # Create a new version
    old_rec_uuid = "a1b2c-3d4e5"
    draft = base_client.post("/records/{}/versions".format(old_rec_uuid))
    assert draft.status_code == 201  # Draft created

    # Get draft id
    rec_uuid = draft.json.get("id", None)
    assert rec_uuid != old_rec_uuid

    # Update with draft content
    draft_content = draft.json.get("metadata")
    # TODO: Add some new metadata
    draft = base_client.put(
        "/records/{}/draft".format(rec_uuid), data=draft_content
    )
    assert draft.status_code == 200

    # Publish record
    action = base_client.post(
        "/records/{}/draft/actions/publish".format(rec_uuid)
    )
    # Accept publishing. Might lunch async tasks.
    # TODO Should be 202
    assert action.status_code == 201

    # Get published record
    record = base_client.get("/records/{}".format(rec_uuid))
    assert record.status_code == 200
    assert record.json.get("id") == rec_uuid

    # TODO: NOT SUPPORTED. OUT OF THE RFC
    # Get the previous version
    # prev_ver = base_client.get(
    #     "/records/{}/versions/{}".format(old_rec_uuid, 1)
    # )
    # assert prev_ver.status_code == 200
    # assert prev_ver.json.get("id") == old_rec_uuid
    # assert prev_ver.json["metadata"]["version"] == "1"

    # # Get the new version
    # curr_ver = base_client.get("/records/{}/versions/{}".format(rec_uuid, 2))
    # assert curr_ver.status_code == 200
    # assert curr_ver.json.get("id") == rec_uuid
    # assert curr_ver.json["metadata"]["version"] == "2"


def test_search_records(base_client):
    """Test search published records."""

    draft = base_client.get("/records")
    assert draft.status_code == 200  # Draft created
    assert len(draft.json.get("hits").get("hits")) == 2

    # TODO: perform a search with terms


def test_search_records_draft(base_client):
    """Test search all records editable by the user."""

    draft = base_client.get("/user/records")
    assert draft.status_code == 200  # Draft created
    assert len(draft.json.get("hits").get("hits")) == 2

    # TODO: perform a search with terms


def test_delete_record(base_client):
    """Test deletion of a published record."""

    draft = base_client.delete("/records/{}".format("a1b2c-3d4e5"))
    # TODO Should be 202
    assert draft.status_code == 204

    # TODO: Implement with permissions (should be admin only)
    # TODO: Assert fails to delete a not published record (draft)
    # TODO: Assert fails to delet a non-existing recid


# TODO: Test case for delete non-published draft
# TODO: Test case for delete published records' draft
# TODO: Test case with external upload of files
# TODO: Missing /records/:id/files/:key/download
