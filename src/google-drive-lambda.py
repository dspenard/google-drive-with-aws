#!/usr/bin/env python

import tempfile
import boto3
import os
import sys
import json

from apiclient import discovery
from apiclient import errors
from apiclient.http import MediaFileUpload

def get_service_account_credentials(credentials_parameter):
    """
    Load Google service account credentials for the specified service account

    Args:
        credentials_parameter: Name of parameter in Parameter Store containing the Google service account credentials json.
    
    Returns: Google service account credential object
    
    https://developers.google.com/identity/protocols/OAuth2ServiceAccount    
    https://google-auth.readthedocs.io/en/latest/_modules/google/oauth2/service_account.html    
    https://developers.google.com/identity/protocols/googlescopes#drivev3
    """
    from google.oauth2 import service_account
    import googleapiclient.discovery

    # get_parameter returns a dictionary object of the json string, so convert it
    # back to a string needed for getting the Google credentials object.
    #
    # Note that WithDecryption=True would be set if using a SecureString in Parameter Store
    ssm_client = boto3.client('ssm')
    creds_dict = ssm_client.get_parameter(Name=credentials_parameter, WithDecryption=False)['Parameter']['Value']
    creds_json = json.loads(creds_dict)

    scopes_list = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
    ]

    credentials = service_account.Credentials.from_service_account_info(creds_json, scopes=scopes_list)
    
    # note for using a credentials json file instead
    # service_account_file = './credentials.json'
    # credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes_list)
            
    return credentials


def get_folder_id(folder_id_parameter):
    """
    Get the Google Drive shared folder ID from Parameter Store
    
    Args:
        folder_id_parameter: Name of parameter in Parameter Store containing the Google Drive shared folder ID.
    
    Returns: folder ID string    
    """
    
    # Note that WithDecryption=True would be set if using a SecureString in Parameter Store
    ssm_client = boto3.client('ssm')
    return ssm_client.get_parameter(Name=folder_id_parameter, WithDecryption=False)['Parameter']['Value']    

    
def upload_file(service, file_name_with_path, file_name, description, folder_id, mime_type):  
    """
    Uploads a file to Google Drive to the designated folder in a shared drive.
    
    Args:
        service: Google Drive API service instance.
        file_name_with_path: Source location of the file just downloaded to the Python tmp folder.
        file_name: Name of file to be saved to Google, and also for its title in the file metadata.
        description: Description of the file to insert, for the file metadata.
        folder_id: Parent folder's ID for the Google Drive shared folder where the file will be uploaded.
        mime_type: MIME type of the file to insert.
    
    Returns: file info
    """
    media_body = MediaFileUpload(file_name_with_path, mimetype=mime_type)

    body = {
        'name': file_name,
        'title': file_name,
        'description': description,
        'mimeType': mime_type,
        'parents': [folder_id]
    }
    
    # note that supportsAllDrives=True is required or else the file upload will fail
    file = service.files().create(
        supportsAllDrives=True,
        body=body,
        media_body=media_body).execute()

    # TODO: Google Drive does not overwrite existing files with a create call,
    # it will add another file with the duplicate name, so add a condition to
    # to do either create or update based on file existence

    # this will work fine, you just have to remove the parents from the body
    # file = service.files().update(
    #     fileId='somefileid',
    #     supportsAllDrives=True,
    #     body=body,
    #     media_body=media_body).execute()

    print('{}, {}'.format(file_name, file['id']))
    
    return file

    
def main_handler(event, context):
    """
    Pull the specified files from S3 and push to a Shared Folder in Google Drive.
    The payload passed in contains a list of Excel file names in the array fileList.
    """
    print('payload:', event)

    bucket = os.environ.get('REPORTS_BUCKET')
    credentials_parameter = os.environ.get('GOOGLE_CREDENTIALS_PARAMETER')
    folder_id_parameter = os.environ.get('GOOGLE_SHARED_FOLDER_ID_PARAMETER')

    credentials = get_service_account_credentials(credentials_parameter)
    folder_id = get_folder_id(folder_id_parameter)
    
    # note regarding cache_discovery=False
    # https://github.com/googleapis/google-api-python-client/issues/299
    service = discovery.build('drive', 'v3', credentials=credentials, cache_discovery=False)

    s3_client = boto3.client('s3')
    
    for file_name in event['fileList']:
        download_path = '/tmp/{}'.format(file_name)
        s3_client.download_file(bucket, file_name, download_path)
        upload_file(service, download_path, file_name, file_name, folder_id, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
