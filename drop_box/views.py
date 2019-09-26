from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from google_drive.models import User
from social_drive import constants
import dropbox

from drives_data.models import DrivesData


class DropBoxHome(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'dropbox_home.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        if user.dropbox_access_token:
            list_of_files = DrivesData.objects.filter(drive_type=DrivesData.DROPBOX, user=request.user)
            return render(request, self.template_name,
                          {'list_of_files': list_of_files, 'drive_type': DrivesData.DROPBOX})
        return redirect(constants.DOPBOX_CONNECT)


class DropBoxReturnURLView(View):
    template_name = 'drop_box_connect.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UpdateDropBoxCredentialsView(View):
    def get(self, request):
        token = request.get_full_path()
        url, token = token.split('/update_drpbox_credentials/?')
        if token:
            credentials_list = token.split('=')
            access_token = credentials_list[1]
            access_token = access_token.replace("&token_type", "")
            user = User.objects.filter(id=request.user.id).first()
            user.dropbox_access_token = access_token
            user.save()
        return redirect('dropbox_home')
