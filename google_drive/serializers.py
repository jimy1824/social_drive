from rest_framework import serializers
from django.contrib.auth import get_user_model
from drives_data.models import DrivesData

UserModel = get_user_model()


class DrivesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivesData
        fields = ('id', 'user', 'drive_type', 'file_type', 'file_id', 'file_name',
                  'file_url', 'sync_id')