from django.contrib import admin
from .models import User,GoogleDriveCredentials
# Register your models here.


class Account(admin.ModelAdmin):
    list_display = ( 'id', 'created_at', 'is_active','first_name', 'last_name', 'email',)
    list_display_links = ('first_name', 'last_name', 'email',)
    search_fields = ('id', 'first_name', 'email')
    ordering = ['-id', ]

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password == orig_obj.password:
                obj.set_password(obj.password)
        else:
             obj.set_password(obj.password)
        obj.save()


class GoogleDriveCredentialsAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'created_at', 'title', 'drive_email',)
    list_display_links = ('id', 'drive_email',)
    search_fields = ('id', 'drive_email')
    ordering = ['-id', ]



admin.site.register(User, Account)
admin.site.register(GoogleDriveCredentials, GoogleDriveCredentialsAdmin)