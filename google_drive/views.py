from io import BytesIO

import joblib as joblib
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.views import View
from django.core.files import File

from .models import User, GoogleDriveCredentials

from social_drive import constants

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from django.contrib.auth.mixins import LoginRequiredMixin


class GoogleDeiveConnect(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'drive_files_list.html'

    def get(self, request, *args, **kwargs):
        creds = None
        user = User.objects.filter(id=request.user.id).first()
        if user.google_credential_file:
            with open(user.google_credential_file.path, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                google_drive_account_instance = GoogleDriveCredentials.objects.filter(
                    drive_email='edtechworxcommunity@gmail.com').first()
                flow = InstalledAppFlow.from_client_secrets_file(
                    google_drive_account_instance.credential_file.path, constants.SCOPES)
                creds = flow.run_local_server(port=0)
                file_name = str(user.id) + '.pickle'
                with open(file_name, 'wb') as token:
                    pickle.dump(creds, token)
                fh = open(file_name, 'rb')
                if fh:
                    # Get the content of the file
                    file_content = ContentFile(fh.read())
                    print(file_content)
                    # Set the media attribute of the article, but under an other path/filename
                    user.google_credential_file.save(file_name, file_content)
                    # Save the article
                    user.save()
                # Close the file and delete it
                fh.close()

                os.remove(file_name)

        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        return render(request, self.template_name, {'items': items})
