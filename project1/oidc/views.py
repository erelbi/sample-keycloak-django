from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import auth
from authlib.integrations.django_client import OAuth


OAUTH = OAuth()
OAUTH.register(
    name='rp',
    client_id=settings.OIDC_CLIENT_ID,
    client_secret=settings.OIDC_CLIENT_SECRET,
    access_token_url=settings.TOKEN_ENDPOINT,
    authorize_url=settings.AUTHORIZATION_ENDPOINT,
    jwks_uri=settings.JWKS_URI,
    client_kwargs={
        'scope': 'openid',
        'code_challenge_method': 'S256',
    },
)


def login_op(request):

    redirect_uri = request.build_absolute_uri(
        reverse_lazy('oidc:login_rp')
    )


    if 'next' in request.GET:
        request.session['url_next_to_login'] = request.GET['next']

  
    return OAUTH.rp.authorize_redirect(request, redirect_uri)


def login_rp(request):
  
    if 'error' in request.GET:
        err_msg = request.GET['error_description']
     

    user = auth.authenticate(request, client=OAUTH.rp)
    if user is not None and user.is_authenticated:
        auth.login(request, user)

        redirect_url = request.session.get('url_next_to_login', settings.LOGIN_REDIRECT_URL)
        if 'url_next_to_login' in request.session:
            del request.session['url_next_to_login']

        return redirect(redirect_url)

   
    return HttpResponse('error')
