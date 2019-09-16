from django.urls import path
from django.conf.urls import include, url
from dropbox import views

urlpatterns = [
    path('dropbox_connect/', views.DropboxConnect.as_view(), name='dropbox_connect'),
    path('connect/', views.ConnectView.as_view(), name='connect'),
]
