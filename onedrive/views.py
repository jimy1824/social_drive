from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from drives_data.models import DrivesData
from google_drive.models import User
from onedrive.auth_helper import get_token_from_code, get_signin_url


class OneDriveHome(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'onedrive_home.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        if user.onedrive_access_code:
            list_of_files = DrivesData.objects.filter(drive_type=DrivesData.ONEDRIVE, user=request.user)
            return render(request, self.template_name,
                          {'list_of_files': list_of_files, 'drive_type': DrivesData.ONEDRIVE})

        redirect_uri = 'http://localhost:8000/gettoken/'
        # redirect_uri = request.build_absolute_uri(reverse('gettoken'))
        sign_in_url = get_signin_url(redirect_uri)
        return redirect(sign_in_url)


def gettoken(request):
    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('gettoken'))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']
    if access_token:
        user = User.objects.filter(email=request.user.email).first()
        user.onedrive_access_code = access_token
        user.save()
    return redirect('onedrive_home')
