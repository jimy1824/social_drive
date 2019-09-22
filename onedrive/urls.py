from django.urls import path
from onedrive import views

urlpatterns = [
    path('onedrive_home/', views.OneDriveHome.as_view(), name='onedrive_home'),
    path('gettoken/', views.gettoken, name='gettoken'),
]
