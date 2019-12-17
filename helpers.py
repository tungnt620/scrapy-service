# -*- coding: utf-8 -*-

from google.cloud import storage


def upload_file_to_google_storage(bucket_name, path_to_source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(path_to_source_file_name)
