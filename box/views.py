import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drives_data.models import DrivesData
from drives_data.serializers import UserSerializer
from drives_data.tasks import data_syscronization
from google_drive.models import User
from social_drive import constants


class BoxHome(APIView):
    login_url = '/login/'
    template_name = 'box_home.html'
    permission_class = (IsAuthenticated,)
    # serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # user = User.objects.filter(id=request.user.id).first()
        # if user.box_access_code:
        #     list_of_files = DrivesData.objects.filter(drive_type=DrivesData.BOX, user=request.user)
        #     return render(request, self.template_name,
        #                   {'list_of_files': list_of_files, 'drive_type': DrivesData.BOX})

        return Response(constants.BOX_CONNECT)


class SaveBoxDataView(APIView):
    permission_class = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        if request.user.box_access_token:
            data_syscronization(DrivesData.BOX, request.user.email)
        return JsonResponse({'msg': 'You are connected'})


class BoxReturnUrl(APIView):
    login_url = '/login/'
    permission_class = (IsAuthenticated, )
    # serializer_class = UserSerializer

    def get(self, request,*args, **kwargs):

        box_access_code = kwargs.get('code')
        print('BOX CODE: ',box_access_code)
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
                data_syscronization(DrivesData.BOX, user.email)
        return JsonResponse({'msg':'Box is connected'})
