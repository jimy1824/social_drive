from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from google_drive.models import User
from social_drive import constants


class DropboxConnect(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'dropbox_home.html'

    def get(self, request, *args, **kwargs):
        print('I am dropbox')
        creds = None
        url_part = '/'+str(request.user.email)+'/'
        return redirect(constants.DOPBOX_CONNECT)

        # return render(request, self.template_name)


class ConnectView(View):
    template_name = 'dropbox_home.html'

    def get(self, request, *args, **kwargs):
        print('I am in connect view')
        creds = None
        user = User.objects.filter(id=request.user.id).first()
        print(dir(request))
        print(dir(request.GET))
        return render(request, self.template_name)
