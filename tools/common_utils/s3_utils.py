from __future__ import print_function
import os
import subprocess
import shlex
import boto3

s3 = boto3.resource('s3')


def download_folder(s3_path, directory_to_download):
    """
    Downloads a folder from s3
    :param s3_path: s3 folder path
    :param directory_to_download: path to download the directory to
    :return: directory that was downloaded
    """
    cmd = 'aws s3 cp --recursive %s %s' % (s3_path, directory_to_download)

    subprocess.check_call(shlex.split(cmd))

    return directory_to_download


def download_file(s3_path, directory_to_download):
    """
    Downloads an object from s3 to a local path
    :param s3_path: s3 object path
    :param directory_to_download: directory to download to
    :return: local file path of the object
    """
    bucket = s3_path.split('/')[2]
    key = '/'.join(s3_path.split('/')[3:])

    object_name = key.split('/')[-1]

    local_file_name = os.path.join(directory_to_download, object_name)

    s3.Object(bucket, key).download_file(local_file_name)

    return local_file_name


def upload_folder(s3_path, local_folder_path, sse=True):
    """
    Uploads a local folder to S3
    :param s3_path: s3 path to upload folder to
    :param local_folder_path: local folder path
    :param sse: boolean whether to enable server-side encryption
    """
    cmd = 'aws s3 cp --recursive %s %s' % (local_folder_path, s3_path)

    if sse:
        cmd += ' --sse'

    subprocess.check_call(shlex.split(cmd))


def upload_file(s3_path, local_path):
    """
    Uploads a local file to s3 with server side encryption enabled
    :param s3_path: s3 object path
    :param local_path: local file path
    :return: response from the upload file
    """
    bucket = s3_path.split('/')[2]
    key = '/'.join(s3_path.split('/')[3:])

    response = s3.Object(bucket, key).upload_file(local_path, ExtraArgs=dict(ServerSideEncryption='AES256'))

    return response
