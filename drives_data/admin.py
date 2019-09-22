from django.contrib import admin
from .models import DrivesData


# Register your models here.


class DrivesDataAdmin(admin.ModelAdmin):
    list_display = ('drive_type', 'id', 'created_at', 'is_active', 'user', 'file_id', 'file_type', 'file_name',)
    list_display_links = ('file_id', 'file_id',)
    search_fields = ('id', 'file_id', 'user__email', 'drive_type')
    ordering = ['-id', ]


admin.site.register(DrivesData, DrivesDataAdmin)
