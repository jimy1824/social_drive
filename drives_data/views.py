import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from drives_data.tasks import data_syscronization
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from drives_data.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings

from google_drive.serializers import DrivesDataSerializer
from .models import User, DrivesData


class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SynchronizationView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        drive_type = kwargs.get('drive_type')
        data_syscronization.delay(drive_type, request.user.email)
        return Response({'messsage': 'success'}, status=HTTP_200_OK)


class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create_user_objects(self, request):
        print('registrations')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        print(email, first_name, last_name, password)
        user = User(first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        response = {'token': token}
        response = json.dumps(response)
        response = json.loads(response)
        return response

    def post(self, request, *args, **kwargs):
        return Response((self.create_user_objects(request)), status=HTTP_200_OK)


class UsersLoggedInView(APIView):
    permission_class = IsAuthenticated
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.request.user).data, status=HTTP_200_OK)


class UsersListView(APIView):
    permission_class = IsAuthenticated
    serializer_class = UserSerializer

    def get_users_list(self, request):
        return User.objects.all()

    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.get_users_list(request), many=True).data, status=HTTP_200_OK)


class UserAvailibilityView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_check_availibility(self, request):
        user = User.objects.filter(email=request.data.get('email')).first()
        response = {'availability': True}
        if user:
            response["availability"] = False
        response = json.dumps(response)
        return json.loads(response)

    def post(self, request, *args, **kwargs):
        return Response(self.get_check_availibility(request), status=HTTP_200_OK)


class DriveDataView(APIView):
    serializers_class = DrivesDataSerializer
    permission_classes = (IsAuthenticated,)

    def get_objects(self, drive_type, request):
        query_dict = {'drive_type': drive_type, 'user': request.user}

        return DrivesData.objects.filter(**query_dict)

    def get(self, request, *args, **kwargs):
        drive_type = kwargs.get('drive_type')
        return Response(
            self.serializers_class(self.get_objects(drive_type, request),many=True).data,status=HTTP_200_OK)
