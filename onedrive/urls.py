from django.urls import path
from onedrive import views

app_name = 'onedrive'
urlpatterns = [
    # path('', views.home, name='home'),
    path('onedrive_home/', views.home, name='onedrive_home'),
    path('gettoken/', views.gettoken, name='gettoken'),
]
