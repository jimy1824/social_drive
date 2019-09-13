from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, max_length=75)
    username = models.CharField(null=True, max_length=150, default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subscription = models.BooleanField(default=False)
    google_credential_file=models.FileField(upload_to='GoogleDriveCredentials/', blank=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return 'Id:{0} Name :{1} {2}, email: {3}'.format(self.id, self.first_name, self.last_name, self.email)





class GoogleDriveCredentials(models.Model):
    drive_email=models.EmailField()
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    credential_file=models.FileField(upload_to='Credentials/', )

    def __str__(self):
        return 'Id:{0} Title:{1} Email:{1} '.format(self.id, self.title,self.drive_email)