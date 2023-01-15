from django.urls import path
from . import views


app_name = 'oidc'
urlpatterns = [
    # API for authentication request
    path('auth/', views.login_op, name='login_op'),
    # redirect endpoint which makes session with RP
    path('login/', views.login_rp, name='login_rp'),
]

