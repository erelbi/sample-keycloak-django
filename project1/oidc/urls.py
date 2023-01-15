from django.urls import path
from . import views


app_name = 'oidc'
urlpatterns = [
 
    path('auth/', views.login_op, name='login_op'),
   
    path('login/', views.login_rp, name='login_rp'),
]

