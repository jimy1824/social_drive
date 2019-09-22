from django.db import models
from google_drive.models import User


# Create your models here.

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DrivesData(BaseModel):
    GOOGLEDRIVE = 'googledrive'
    ONEDRIVE = 'onedrive'
    DROPBOX = 'dropbox'
    BOX = 'box'
    EVERNOTE = 'evernote'
    TYPE = (
        (GOOGLEDRIVE, 'Google Drive'),
        (ONEDRIVE, 'One Drive'),
        (DROPBOX, 'DropBox'),
        (BOX, 'box'),
        (EVERNOTE, 'EverNote'),
    )
    DIRECTORY = 'directory'
    FILE = 'file'
    FILETYPE = (
        (DIRECTORY, 'Directory'),
        (FILE, 'File'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drive_type = models.CharField(max_length=30, choices=TYPE)
    file_type = models.CharField(max_length=30, choices=FILETYPE)
    file_id = models.CharField(max_length=1000)
    file_name = models.CharField(max_length=1000)
    file_url = models.URLField(blank=True, null=True)
    sync_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.user.email)
