from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from drives_data.tasks import data_syscronization


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
