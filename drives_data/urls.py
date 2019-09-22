from django.urls import path
from drives_data import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('syncronization/<str:drive_type>', views.SynchronizationView.as_view(), name='syncronization'),
]
