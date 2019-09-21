from django.urls import path
from django.conf.urls import include, url
from box import views

urlpatterns = [
    path('box_connect/', views.BoxConnect.as_view(), name='box_connect'),
    path('box_home/', views.BoxHome.as_view(), name='box_home'),
]
