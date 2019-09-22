from urllib.parse import quote, urlencode
import requests
import time

# Client ID and secret
client_id = 'ce9a9b0e-6de2-4ba1-bcfa-1352be652529'
client_secret = 'ujIp-k_-R0Xm[J0zCpS77fx*OPVph]AY'

# Constant strings for OAuth2 flow
# The OAuth authority
authority = 'https://login.microsoftonline.com'

# GET https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=ce9a9b0e-6de2-4ba1-bcfa-1352be652529&scope=openid offline_access User.Read files.read files.read.all files.readwrite files.readwrite.all&response_type=token&redirect_uri=https://www.google.com


# The authorize URL that initiates the OAuth2 client credential flow for admin consent
authorize_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/authorize?{0}')

# The token issuing endpoint
token_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/token')

# The scopes required by the app
scopes = ['openid',
          'offline_access',
          'User.Read',
          'files.read',
          'files.read.all',
          'files.readwrite',
          'files.readwrite.all']


def get_signin_url(redirect_uri):
    # Build the query parameters for the signin url
    params = {'client_id': client_id,
              'redirect_uri': redirect_uri,
              'response_type': 'code',
              'scope': ' '.join(str(i) for i in scopes)
              }

    signin_url = authorize_url.format(urlencode(params))
    # print(signin_url)

    return signin_url


def get_token_from_code(auth_code, redirect_uri):
    # Build the post form for the token request
    post_data = {'grant_type': 'authorization_code',
                 'code': auth_code,
                 'redirect_uri': redirect_uri,
                 'scope': ' '.join(str(i) for i in scopes),
                 'client_id': client_id,
                 'client_secret': client_secret
                 }

    r = requests.post(token_url, data=post_data)

    try:
        return r.json()
    except:
        return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)


def get_token_from_refresh_token(refresh_token, redirect_uri):
    # Build the post form for the token request
    post_data = {'grant_type': 'refresh_token',
                 'refresh_token': refresh_token,
                 'redirect_uri': redirect_uri,
                 'scope': ' '.join(str(i) for i in scopes),
                 'client_id': client_id,
                 'client_secret': client_secret
                 }

    r = requests.post(token_url, data=post_data)
    print(r.json())

    try:
        return r.json()
    except:
        return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)


def get_access_token(request, redirect_uri):
    current_token = request.session.get('access_token')
    expiration = request.session.get('token_expires')
    now = int(time.time())
    if current_token and now < expiration:
        # Token still valid
        return current_token
    else:
        # Token expired
        refresh_token = request.session.get('refresh_token')
        new_tokens = get_token_from_refresh_token(refresh_token, redirect_uri)

        # Update session
        # expires_in is in seconds
        # Get current timestamp (seconds since Unix Epoch) and
        # add expires_in to get expiration time
        # Subtract 5 minutes to allow for clock differences
        expiration = int(time.time()) + 3600 - 300

        # Save the token in the session
        request.session['access_token'] = new_tokens['access_token']
        request.session['refresh_token'] = new_tokens['refresh_token']
        request.session['token_expires'] = expiration

        return new_tokens['access_token']
