import boto3
from botocore.exceptions import NoCredentialsError
import os

MINIO_STORAGE_ENDPOINT = os.getenv("MINIO_STORAGE_ENDPOINT")
MINIO_STORAGE_ACCESS_KEY = os.getenv("MINIO_STORAGE_ACCESS_KEY")
MINIO_STORAGE_SECRET_KEY = os.getenv("MINIO_STORAGE_SECRET_KEY")
MINIO_BUCKET_NAME = "profile-bucket"

s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{MINIO_STORAGE_ENDPOINT}",
    aws_access_key_id=MINIO_STORAGE_ACCESS_KEY,
    aws_secret_access_key=MINIO_STORAGE_SECRET_KEY,
)


def upload_file(file_path, object_name):
    try:
        s3.upload_file(file_path, MINIO_BUCKET_NAME, object_name)
        print(f"File '{file_path}' uploaded successfully as '{object_name}'")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"Error uploading file: {e}")


def download_file(object_name, download_path):
    try:
        s3.download_file(MINIO_BUCKET_NAME, object_name, download_path)
        print(f"File '{object_name}' downloaded successfully to '{download_path}'")
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"Error downloading file: {e}")


def generate_presigned_url(object_name, expiration=3600):
    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": MINIO_BUCKET_NAME, "Key": object_name},
            ExpiresIn=expiration,
        )
        print(f"Pre-signed URL: {url}")
        return url
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")


upload_file(
    "blog_post_management_system/static/profiles/profile_pictures/1.jpg", "Object1.jpg"
)
download_file(
    "Object1.jpg",
    "blog_post_management_system/static/profiles/profile_pictures/Object1.jpg",
)
generate_presigned_url("Object1.jpg")
