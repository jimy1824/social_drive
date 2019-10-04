# social_drive

RESTful API endpoint to provide data from Onedrive, Google Drive, Dropbox, Box, Microsoft SharePoint, Google Cloud, and Azure AD. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

github link for get clone or download repository (public repository)

```
https://github.com/tahirawan4/social_drive.git

```

### Installing

1. Install python, project require python 3.6/3.7 install python
2. Create virtual environment
    1. Install pip first
        ```
        sudo apt-get install python3-pip
        ```
    2. Then install virtualenv using pip3
        ```
       sudo pip3 install virtualenv
        ```
    3. create a virtual environment
        ```
         virtualenv venv
        ```
        for specific Python interpreter  choice
        ```
          virtualenv -p /usr/bin/python3.6 venv
        ```
    4. Activate virtual environment
        ``` 
        source venv/bin/activate
        ```
3. Install requirements
```
command pip install -r requirements.txt
```

## Run Server
Run the server
```
python manage.py runserver
```

## Running the tests

Run test cases 
```
python manage.py test
```

## Built With

* [Azure Portal](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade) - Create an application for onedrive then and set the redirect URI as 
    ```
    https://domainname.com/gettoken
    ``` 
    or 
    ```
    http://localhost:8000/gettoken
    ```
    or you can see this documentation 
    ```
    https://docs.microsoft.com/en-us/onedrive/developer/rest-api/getting-started/app-registration?view=odsp-graph-online
    ```
    Also copy and paste the clientID and Secert key ID into your django project's .env file.
        
* [Google Cloud](https://cloud.google.com) - Create application and enable the APIs to use SDK of Google Cloud.
    After enabling the API, download the `credentials.json` file, and keep it in this path `social_drive/credentials/credentials.json` of your django application.
* [Dropbox](https://www.dropbox.com/developers/apps?_tk=pilot_lp&_ad=topbar4&_camp=myapps) - Register an app here, and set the redirect uri as home page of your vue application
    ```
    http:localhost:8080/
    ```
    Also copy and paste the clientID and Secert key ID into your django project's .env file. 
* [Box](https://developer.box.com/reference) - here you can find all the documentation of the box api and sdk.
    Register your application here, [Box Developer Console](https://app.box.com/developers/console).
    Make the redirect uri like this, to redirect the user on to the home page of Vue application after authentication.
    ```
    http:localhost:8080/
    ```    
    Also copy and paste the clientID and Secert key ID into your django project's .env file.
