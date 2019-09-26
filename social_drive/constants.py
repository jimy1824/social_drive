from django.conf import settings

SERVER_ADDRESS = 'http://127.0.0.1:8000'
DROPBOX_RETRUN_URI = SERVER_ADDRESS + '/connect/'
BOX_RETRUN_URI = SERVER_ADDRESS + '/box_retrun_url/'
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
DOPBOX_CONNECT = 'https://www.dropbox.com/oauth2/authorize?client_id=' + settings.DROPBOX_CLIENT_ID + '&response_type=token&redirect_uri=' + DROPBOX_RETRUN_URI
BOX_CONNECT = 'https://account.box.com/api/oauth2/authorize?response_type=code&client_id=' + settings.BOX_CLIENT_ID + '&redirect_uri=' + BOX_RETRUN_URI + '&state=' + settings.BOX_STATE_ID
BOX_AUTH_URL = 'https://api.box.com/oauth2/token'
