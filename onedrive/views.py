from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from onedrive.auth_helper import get_token_from_code, get_signin_url
from onedrive.ondrive_service import get_me


def home(request):
  # redirect_uri = request.build_absolute_uri(reverse('onedrive:gettoken'))
  redirect_uri = 'https://79fe3397.ngrok.io/gettoken/'
  sign_in_url = get_signin_url(redirect_uri)
  context = { 'signin_url': sign_in_url }
  return render(request, 'home.html', context)


def gettoken(request):
  auth_code = request.GET['code']
  # redirect_uri = request.build_absolute_uri(reverse('onedrive:gettoken'))
  # redirect_uri = request.build_absolute_uri(reverse('https://www.google.com'))
  redirect_uri = 'https://79fe3397.ngrok.io/gettoken/'
  token = get_token_from_code(auth_code, redirect_uri)
  print(token)
  access_token = token['access_token']
  user = get_me(access_token)

  # Save the token in the session
  request.session['access_token'] = access_token
  return HttpResponse('User: {0}, Access token: {1}'.format(user['displayName'], access_token))
