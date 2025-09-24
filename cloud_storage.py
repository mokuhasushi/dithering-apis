import os

from google.cloud import storage

BUCKET_NAME = os.environ.get('GC_BUCKET')

def prepare_blob(destination):
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    return bucket.blob(destination)


def upload_blob_from_file(file, destination_folder="uploaded/"):
    """Uploads a file to the bucket, return uploaded url."""

    blob = prepare_blob(f"{destination_folder}{file.filename}")

    blob.upload_from_file(file.file)

    return blob.public_url

def upload_blob_from_string(img_blob, filename, destination_folder="uploaded/"):
    """Uploads a (byte) string to the bucket, return uploaded url."""

    blob = prepare_blob(f"{destination_folder}{filename}")

    blob.upload_from_string(img_blob)

    return blob.public_url

def upload_blob(source_file_name, blob_name, destination_folder="uploaded/"):
    """Uploads a file from filetree to the bucket, return uploaded url."""

    blob = prepare_blob(f"{destination_folder}{blob_name}")

    blob.upload_from_filename(source_file_name)

    return blob.public_url
