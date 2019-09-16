from django.urls import path
from django.conf.urls import include, url
from google_drive import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('connect_google_drive/', views.GoogleDriveConnect.as_view(), name='connect_google_drive'),
]
