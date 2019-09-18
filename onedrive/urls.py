from django.urls import path
from django.conf.urls import include, url
from onedrive import views

urlpatterns = [
    path('onedrive_honme/', views.OneDriveView.as_view(), name='onedrive_honme'),
    # path('connect/', views.ConnectView.as_view(), name='connect'),
]
