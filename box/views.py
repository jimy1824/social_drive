import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from drives_data.models import DrivesData
from google_drive.models import User
from social_drive import constants


class BoxHome(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'box_home.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        if user.box_access_code:
            list_of_files = DrivesData.objects.filter(drive_type=DrivesData.BOX, user=request.user)
            return render(request, self.template_name,
                          {'list_of_files': list_of_files, 'drive_type': DrivesData.BOX})
        return redirect(constants.BOX_CONNECT)


class BoxReturnUrl(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        box_access_code = request.GET.get('code')
        if box_access_code:
            r = requests.post(constants.BOX_AUTH_URL,
                              data={'grant_type': 'authorization_code', 'code': box_access_code,
                                    'client_id': settings.BOX_CLIENT_ID,
                                    'client_secret': settings.BOX_CLIENT_SECRET_ID})
            r_object = r.json()
            refresh_token = r_object['refresh_token']
            if refresh_token:
                user = User.objects.filter(email=request.user.email).first()
                user.box_access_code = refresh_token
                user.save()
        return redirect('box_home')
