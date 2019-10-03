from django.urls import path
from django.conf.urls import include, url
from google_drive import views

urlpatterns = [
    path('googledrive/', views.GoogleDriveHome.as_view(), name='googledrive_home'),
    path('googledrive/<int:user_id>/', views.GoogleDriveHomeUser.as_view(), name='googledrive_home_user'),
    path('connect_google_drive/', views.GoogleDriveConnect.as_view(), name='connect_google_drive'),
]
