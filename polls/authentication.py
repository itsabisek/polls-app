"""

    authentication.py: Handles the authentication and session management using JSON Web Tokens.
    Contains helper methods to create token, validate token and retrievig the payload of a token

"""


from rest_framework.exceptions import AuthenticationFailed
from rest_framework import authentication
from django.http import HttpResponseForbidden
from datetime import datetime, timedelta
import jwt
from .models import User
from functools import wraps


# Base class containing all the helper methods
class JWTUtils():

    def __init__(self):
        self._SECRET_KEY = 'POLLS_APP_SECRET_KEY'
        self._TOKEN_EXPIRE_TIME = 24

    def authenticate(self, request):
        """
            Method to vaidate a token in the request headers. Raises an exception if token
            is not found in request header, invalid token or expired token

        """

        try:
            token = request.META['HTTP_AUTHORIZATION'].split(" ")[-1]
            jwt.decode(token, self._SECRET_KEY, algorithms=['HS256'])
            return True
        except KeyError:
            raise AuthenticationFailed("Token not found in header")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has an expired signature")
        except jwt.InvalidSignatureError:
            raise AuthenticationFailed(
                "Signature of token could not be validated")

        return False

    def generate_token(self, claim):
        """
            Generates a token with the claim as the payload. The token will be valid for
            24 hours by default

        """

        _expiry = datetime.utcnow() + timedelta(hours=self._TOKEN_EXPIRE_TIME)
        payload = {"exp": _expiry, 'id': claim}
        token = jwt.encode(payload, self._SECRET_KEY, algorithm="HS256")
        return token

    def get_claim(self, request):
        """
            Returns the payload inside the token in the request. Raises an exception if 
            token is not found in the request headers

        """
        try:
            token = request.META['HTTP_AUTHORIZATION'].split(" ")[-1]
            return jwt.decode(token, self._SECRET_KEY, algorithms=['HS256']).get('id')
        except KeyError:
            raise AuthenticationFailed("Token not found in header")


class JSONWebTokenAuthentication(authentication.BaseAuthentication):
    """
        Custom authentication class that extends BaseAuthentication class of
        rest_framework. .authenticate() method is overriden to check for JWT
        in header and validate the signature of the token and return the User 
        instance by getting the uuid from the token payload

    """

    def authenticate(self, request):
        try:
            user = None
            authenticator = JWTUtils()
            is_auth = authenticator.authenticate(request)
            if is_auth:
                claim = authenticator.get_claim(request)
                if claim is not None:
                    user = User.objects.get(uuid=claim)
                print user.username

        except User.DoesNotExist as e:
            raise AuthenticationFailed("User doesn't exist. %s" % e)

        except Exception as e:
            raise e

        finally:
            return (user, None)
