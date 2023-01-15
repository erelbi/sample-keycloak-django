from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class OidcBackend(BaseBackend):
 
    def authenticate(self, request, client=None):
  
        if client is None:
            return None

       
        token = client.authorize_access_token(request)

        
        if token and 'userinfo' in token:
            assert 'preferred_username' in token['userinfo']
            username = token['userinfo']['preferred_username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.is_staff = False
                user.is_superuser = False
                user.save()
            return user

     
        return None

    def get_user(self, user_id):
  
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
