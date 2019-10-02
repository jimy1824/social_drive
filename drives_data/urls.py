from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from drives_data import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('syncronization/<str:drive_type>', views.SynchronizationView.as_view(), name='syncronization'),
    path('login/', obtain_jwt_token),
    path('refresh-token', refresh_jwt_token),
    re_path(r'^api-token-refresh/', refresh_jwt_token),
    re_path(r'^api-token-verify/', verify_jwt_token),
    path('registration/', views.RegistrationView.as_view()),
    path('user-list/', views.UsersListView.as_view()),
    path('user-availibility/', views.UserAvailibilityView.as_view()),
]
