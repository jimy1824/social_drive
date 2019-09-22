from django.urls import path
from django.conf.urls import include, url
from evernote_drive import views

urlpatterns = [
    path('evernote_connect/', views.EvernoteConnect.as_view(), name='evernote_connect'),
    # path('evernote_home/', views.EvernoteHome.as_view(), name='evernote_home'),
]
