from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class OidcBackend(BaseBackend):
    """
    custom backend for OIDC
    """
    def authenticate(self, request, client=None):
        """
        overriding method.

        params
            client: OAuth client of Authlib
        """
        if client is None:
            return None

        # token request
        token = client.authorize_access_token(request)

        # makes django user according to ID token
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

        # some error handling
        # ...
        return None

    def get_user(self, user_id):
        """
        overriding method.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
