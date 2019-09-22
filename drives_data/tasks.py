from social_drive.celery import app
from google_drive.models import User
from .models import DrivesData
import dropbox

import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def Dropbox_syscronization(user, access_token):
    data_list = []
    dbx = dropbox.Dropbox(access_token)
    get_file_of_specific_folder(user, data_list, dbx, '')
    for data_dict in data_list:
        instance = DrivesData(**data_dict)
        instance.save()


def get_file_of_specific_folder(user, data_list, dbx, folder_path):
    folders = dbx.files_list_folder(folder_path)
    for sub_folder in folders.entries:
        if isinstance(sub_folder, dropbox.files.FileMetadata):
            data_dict = {'user': user, 'drive_type': DrivesData.DROPBOX, 'file_id': sub_folder.id,
                         'file_name': sub_folder.name, 'file_type': DrivesData.FILE}
            data_list.append(data_dict)
        else:
            data_dict = {'user': user, 'drive_type': DrivesData.DROPBOX, 'file_id': sub_folder.id,
                         'file_name': sub_folder.name, 'file_type': DrivesData.DIRECTORY}
            data_list.append(data_dict)
            get_file_of_specific_folder(user, data_list, dbx, sub_folder.path_lower)


def GoogleDrive_syscronization(user):
    creds = None
    if user.google_credential_file:
        with open(user.google_credential_file.path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(
        pageSize=25, fields="nextPageToken, files(id, name)").execute()
    data_list = results.get('files', [])
    for file in data_list:
        instance = DrivesData(user=user, drive_type=DrivesData.GOOGLEDRIVE, file_type=DrivesData.FILE,
                              file_id=file.get('id'), file_name=file.get('name'))
        instance.save()


@app.task
def data_syscronization(drive_type, user_email):
    user = User.objects.filter(email=user_email).first()
    if user.dropbox_access_token:
        if drive_type == DrivesData.DROPBOX:
            Dropbox_syscronization(user, user.dropbox_access_token)
    if user.google_credential_file:
        if drive_type == DrivesData.GOOGLEDRIVE:
            GoogleDrive_syscronization(user)
