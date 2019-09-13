from django.urls import path
from django.conf.urls import include, url
from google_drive import views

urlpatterns = [
    path('', views.GoogleDeiveConnect.as_view(), name='connect_google_drive'),

]
