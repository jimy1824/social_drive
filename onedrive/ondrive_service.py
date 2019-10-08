import requests
import uuid
import json

graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'


# Generic API Sending
def make_api_call(method, url, token, payload=None, parameters=None):
    # Send these headers with all API calls
    headers = {'User-Agent': 'django_onedrive/1.0',
               'Authorization': 'Bearer {}'.format(token),
               'Accept': 'application/json',
               "Content-Type": "application/x-www-form-urlencoded"}

    # Use these headers to instrument calls. Makes it easier
    # to correlate requests and responses in case of problems
    # and is a recommended best practice.
    request_id = str(uuid.uuid4())
    instrumentation = {'client-request-id': request_id,
                       'return-client-request-id': 'true'}

    headers.update(instrumentation)

    response = None

    if (method.upper() == 'GET'):
        response = requests.get(url, headers=headers, params=parameters)
    elif (method.upper() == 'DELETE'):
        response = requests.delete(url, headers=headers, params=parameters)
    elif (method.upper() == 'PATCH'):
        headers.update({'Content-Type': 'application/json'})
        response = requests.patch(url, headers=headers, data=json.dumps(payload), params=parameters)
    elif (method.upper() == 'POST'):
        headers.update({'Content-Type': 'application/json'})
        response = requests.post(url, headers=headers, data=json.dumps(payload), params=parameters)

    return response


def get_me(access_token):
    get_me_url = graph_endpoint.format('/me')

    # Use OData query parameters to control the results
    #  - Only return the displayName and mail fields
    query_parameters = {'$select': 'displayName,files'}

    r = make_api_call('GET', get_me_url, access_token, "", parameters=query_parameters)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)


def get_drive(access_token):
    get_me_url = graph_endpoint.format('/me/drive/root/children')

    # Use OData query parameters to control the results
    #  - Only return the displayName and mail fields
    query_parameters = {}

    r = make_api_call('GET', get_me_url, access_token, "", parameters=query_parameters)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)


def get_sharepoint_site_id(access_token):
    # get_me_url = graph_endpoint.format('/sites/netorg225728.sharepoint.com,e93cb13b-eda5-4fdd-8905-52d579965644,cc542cd1-b287-45fe-9048-4b8e2e6c5bbe')
    # get_me_url = graph_endpoint.format('/sites/root/lists')
    get_me_url = graph_endpoint.format('/sites/root/lists')
    # get_me_url = graph_endpoint.format('/sites/netorg225728.sharepoint.com,e93cb13b-eda5-4fdd-8905-52d579965644,cc542cd1-b287-45fe-9048-4b8e2e6c5bbe/drives/b!O7E86aXt3U-JBVLVeZZWRNEsVMyHsv5FkEhLji5sW76toYeV8uUqRKEwRYeRIVHy/root/children')

    # Use OData query parameters to control the results
    #  - Only return the displayName and mail fields
    query_parameters = {}

    r = make_api_call('GET', get_me_url, access_token, "", parameters=query_parameters)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)


def get_sharepoint_drive_id(access_token, site_id):
    get_me_url = graph_endpoint.format('/sites/'+site_id+'/drives')
    # get_me_url = graph_endpoint.format('/sites/root/lists')
    # get_me_url = graph_endpoint.format('/sites/root/lists')
    # get_me_url = graph_endpoint.format('/sites/netorg225728.sharepoint.com,e93cb13b-eda5-4fdd-8905-52d579965644,cc542cd1-b287-45fe-9048-4b8e2e6c5bbe/drives/b!O7E86aXt3U-JBVLVeZZWRNEsVMyHsv5FkEhLji5sW76toYeV8uUqRKEwRYeRIVHy/root/children')

    # Use OData query parameters to control the results
    #  - Only return the displayName and mail fields
    query_parameters = {}

    r = make_api_call('GET', get_me_url, access_token, "", parameters=query_parameters)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)


def get_sharepoint(access_token, site_id, drive_id):
    get_me_url = graph_endpoint.format('/sites/'+site_id+'/drives/'+drive_id+'/root/children')

    # Use OData query parameters to control the results
    #  - Only return the displayName and mail fields
    query_parameters = {}

    r = make_api_call('GET', get_me_url, access_token, "", parameters=query_parameters)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)
