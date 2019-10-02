from django.urls import path
from onedrive import views

urlpatterns = [
    path('onedrive_home/', views.OneDriveHome.as_view(), name='onedrive_home'),
    path('gettoken/', views.GetToken.as_view(), name='gettoken'),
    path('save_token/', views.SaveToken.as_view(), name='save_token'),
]
