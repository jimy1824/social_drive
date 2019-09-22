from django.urls import path
from django.conf.urls import include, url
from box import views

urlpatterns = [
    path('box_retrun_url/', views.BoxReturnUrl.as_view(), name='box_retrun_url'),
    path('box_home/', views.BoxHome.as_view(), name='box_home'),
]
