from django.urls import path
from django.conf.urls import include, url
from google_drive import views

urlpatterns = [
    path('googledrive/', views.GoogleDriveHome.as_view(), name='googledrive_home'),
    path('connect_google_drive/', views.GoogleDriveConnect.as_view(), name='connect_google_drive'),
]
