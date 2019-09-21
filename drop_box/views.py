from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from google_drive.models import User
from social_drive import constants
import dropbox

class DropBoxHome(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'dropbox_home.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        if user.dropbox_access_token:
            dbx = dropbox.Dropbox(user.dropbox_access_token)
            account_info=dbx.users_get_current_account()
            total_files=dbx.file_requests_count()
            list_of_files=dbx.files_list_folder('').entries
            return render(request, self.template_name, {'total_files': total_files,'account_info':account_info,'list_of_files':list_of_files})
        return redirect(constants.DOPBOX_CONNECT)




class DropBoxReturnURLView(View):
    template_name = 'drop_box_connect.html'

    def get(self, request,*args, **kwargs):
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
            user.dropbox_access_token=access_token
            user.save()
        return redirect('dropbox_home')
