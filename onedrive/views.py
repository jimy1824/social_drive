import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from drives_data.models import DrivesData
from drives_data.serializers import UserSerializer
from google_drive.models import User
from onedrive.auth_helper import get_token_from_code, get_signin_url, get_code_from_code
from onedrive.ondrive_service import get_sharepoint, get_drive

from social_drive import constants


class OneDriveHome(APIView):
    login_url = '/login/'
    template_name = 'onedrive_home.html'
    permission_class = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        # user = User.objects.filter(id=request.user.id).first()
        # if user.onedrive_access_code:
        #     list_of_files = DrivesData.objects.filter(drive_type=DrivesData.ONEDRIVE, user=request.user)
        #     return render(request, self.template_name,
        #                   {'list_of_files': list_of_files, 'drive_type': DrivesData.ONEDRIVE})

        redirect_uri = 'https://2ea8349c.ngrok.io/gettoken/'
        # redirect_uri = request.build_absolute_uri(reverse('gettoken'))
        sign_in_url = get_signin_url(redirect_uri)
        return Response(sign_in_url)


class GetToken(View):

    def get(self, request):
        auth_code = request.GET['code']
        # redirect_uri = request.build_absolute_uri(reverse('gettoken'))
        redirect_uri = 'https://2ea8349c.ngrok.io/gettoken/'
        token = get_token_from_code(auth_code, redirect_uri)
        # token = get_code_from_code(auth_code, redirect_uri)
        access_token = token['access_token']

        # sharepoint = get_sharepoint(access_token)
        # print(sharepoint)
        # values = sharepoint['value']
        # for i in range(len(values)):
        #     print(values[i]['list'])
        #     print(values[i]['webUrl'])
        return redirect('http://localhost:8080/onedrive/?access_token='+access_token)


class SaveToken(APIView):
    permission_class = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        access_token = request.GET.get('access_token')
        # access_token = access_token.replace('%20', '')
        data = get_drive(access_token)
        print(data)
        sharepoint = get_sharepoint(access_token)
        print(sharepoint)
        if access_token:
            user = User.objects.filter(email=request.user.email).first()
            user.onedrive_access_code = access_token
            user.save()
        return redirect('http://localhost:8080/onedrive/')