from onedrive.ondrive_service import get_drive
from social_drive.celery import app
from google_drive.models import User
from .models import DrivesData
import dropbox

import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import requests


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


def Box_syscronization(user):
    if user.box_access_code:
        r = requests.post("https://api.box.com/oauth2/token",
                          data={'grant_type': 'refresh_token', 'refresh_token': user.box_access_code,
                                'client_id': 'vtqh4e0myek3bpx7t2mdwca19xz6rgb5',
                                'client_secret': 'knlLggbUFmO6VMRqKg4nAonHW5ZE1Zaa'})
        r_object = r.json()
        refresh_token = r_object['refresh_token']
        if refresh_token:
            user.box_access_code = refresh_token
            user.save()
        access_token = r_object['access_token']
        data = {"Authorization": "Bearer " + access_token}
        files = requests.get('https://api.box.com/2.0/folders/0', headers=data)
        files_entries = files.json().get('item_collection').get('entries')
        for file in files_entries:
            if file.get('type') == 'folder':
                file_type = DrivesData.DIRECTORY
            else:
                file_type = DrivesData.FILE
            instance = DrivesData(user=user, drive_type=DrivesData.BOX, file_type=file_type,
                                  file_id=file.get('id'), file_name=file.get('name'))
            instance.save()


def OneDrive_syscronization(user, onedrive_access_code):
    raw_data = get_drive(onedrive_access_code)
    for file in raw_data.get('value'):
        file_type = DrivesData.FILE
        if file.get('folder'):
            file_type = DrivesData.DIRECTORY
        if file.get('file'):
            file_type = DrivesData.FILE
        instance = DrivesData(user=user, drive_type=DrivesData.ONEDRIVE, file_type=file_type, file_id=file.get('id'),
                              file_name=file.get('name'))
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
    if user.box_access_code:
        if drive_type == DrivesData.BOX:
            Box_syscronization(user)
    if user.onedrive_access_code:
        if drive_type == DrivesData.ONEDRIVE:
            OneDrive_syscronization(user, user.onedrive_access_code)
