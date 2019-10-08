from django.urls import path
from django.conf.urls import include, url
from ever_note import views

urlpatterns = [
    path('evernote_home/', views.EvernoteHome.as_view(), name='evernote_home'),
    path('evernote_connect/', views.EvernoteHome.as_view(), name='evernote_connect'),
]
