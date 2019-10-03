from django.urls import path
from django.conf.urls import include, url
from drop_box import views

urlpatterns = [
    path('dropbox_home/', views.DropBoxHome.as_view(), name='dropbox_home'),
    path('connect/', views.DropBoxReturnURLView.as_view(), name='connect'),
    path('update_drpbox_credentials/', views.UpdateDropBoxCredentialsView.as_view(), name='update_drpbox_credentials'),
    path('save_dropbox_data/', views.SaveDropboxDataView.as_view(), name='save_dropbox_data'),
]
