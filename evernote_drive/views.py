import requests
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from google_drive.models import User
from social_drive import constants
from evernote.api.client import EvernoteClient


class EvernoteConnect(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'dropbox_home.html'

    def get(self, request, *args, **kwargs):
        client = EvernoteClient(
            consumer_key='junaidtariq-8730',
            consumer_secret='2be19523b71b0d91',
            sandbox=True  # Default: True
        )
        request_token = client.get_request_token('https://www.google.com')
        return redirect(client.get_authorize_url(request_token))


# class EvernoteHome(LoginRequiredMixin, View):
#     login_url = '/login/'
#     template_name = 'box_home.html'
#
#     def get(self, request, *args, **kwargs):
#         print('I am connected with Box')
#         # import pdb;pdb.set_trace()
#         code = request.GET.get('code')
#         r = requests.post("https://api.box.com/oauth2/token", data={'grant_type': 'authorization_code', 'code': code,
#                                                                     'client_id': 'vtqh4e0myek3bpx7t2mdwca19xz6rgb5',
#                                                                     'client_secret': 'knlLggbUFmO6VMRqKg4nAonHW5ZE1Zaa'})
#         r_object = r.json()
#         access_token = r_object['access_token']
#         data = {"Authorization":"Bearer "+access_token}
#         files = requests.get('https://api.box.com/2.0/folders/0', headers=data)
#         print(files.json())
#         return render(request, self.template_name)
