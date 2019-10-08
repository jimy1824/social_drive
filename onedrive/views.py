import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from drives_data.models import DrivesData
from drives_data.serializers import UserSerializer
from drives_data.tasks import data_syscronization, SharePoint_syscronization
from google_drive.models import User
from onedrive.auth_helper import get_token_from_code, get_signin_url, get_code_from_code
from onedrive.ondrive_service import get_drive, get_sharepoint_site_id, get_sharepoint_drive_id, get_sharepoint
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

        User.objects.filter(id=request.user.id).update(currently_active=True)
        redirect_uri = 'https://27e84f99.ngrok.io/gettoken/'
        sign_in_url = get_signin_url(redirect_uri)
        # redirect_uri = reverse('gettoken', args=[request.user.id])
        print(sign_in_url)
        return Response(sign_in_url)


class GetToken(View):

    def get(self, request):
        auth_code = request.GET['code']
        # redirect_uri = request.build_absolute_uri(reverse('gettoken'))
        redirect_uri = 'https://27e84f99.ngrok.io/gettoken/'
        token = get_token_from_code(auth_code, redirect_uri)
        # token = get_code_from_code(auth_code, redirect_uri)
        access_token = token['access_token']
        data = get_drive(access_token)
        sharepoint = get_sharepoint_site_id(access_token)
        site_id = sharepoint['value'][0]['parentReference']['siteId']
        sharepoint = get_sharepoint_drive_id(access_token, site_id)
        drive_id = sharepoint['value'][0]['id']
        sharepoint = get_sharepoint(access_token, site_id, drive_id)
        user = User.objects.filter(currently_active=True)
        SharePoint_syscronization(user[0], sharepoint)
        return redirect('http://localhost:8080/?access_token='+access_token)


class SaveToken(APIView):
    permission_class = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        access_token = request.GET.get('access_token')
        # access_token = access_token.replace('%20', '')
        # data = get_drive(access_token)
        # print(data)
        # sharepoint = get_sharepoint(access_token)
        # print(sharepoint)
        if access_token:
            user = User.objects.filter(email=request.user.email).first()
            user.onedrive_access_code = access_token
            user.save()
            # data_syscronization(DrivesData.ONEDRIVE, user.email)
        return redirect('http://localhost:8080/onedrive/')