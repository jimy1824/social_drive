from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'google_credential_file', 'dropbox_access_token',
                  'box_access_code', 'onedrive_access_code')