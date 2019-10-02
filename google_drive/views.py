import pickle
import os.path
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.views import View
from django.core.files import File
from .models import User, GoogleDriveCredentials
from social_drive import constants
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.contrib.auth.mixins import LoginRequiredMixin
from drives_data.models import DrivesData


class GoogleDriveHome(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'googledrive_home.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        if user.google_credential_file:
            list_of_files = DrivesData.objects.filter(drive_type=DrivesData.GOOGLEDRIVE, user=request.user)
            return render(request, self.template_name,
                          {'list_of_files': list_of_files, 'drive_type': DrivesData.GOOGLEDRIVE})
        return redirect('connect_google_drive')


class GoogleDriveConnect(LoginRequiredMixin, View):
    login_url = '/login/'

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
                flow = InstalledAppFlow.from_client_secrets_file('social_drive/credentials/credentials.json',
                                                                 constants.SCOPES)
                creds = flow.run_local_server(port=0)
                file_name = str(user.id) + '.pickle'
                with open(file_name, 'wb') as token:
                    pickle.dump(creds, token)
                fh = open(file_name, 'rb')
                if fh:
                    file_content = ContentFile(fh.read())
                    user.google_credential_file.save(file_name, file_content)
                    user.save()
                fh.close()

                os.remove(file_name)
        return redirect('googledrive_home')
