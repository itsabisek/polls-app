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
from utils import authenticate_token, get_current_time, get_token_payload, generate_token


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
            is_auth = authenticate_token(request)
            if is_auth:
                claim = get_token_payload(request)
                if claim is not None:
                    user = User.objects.get(uuid=claim)

        except User.DoesNotExist as e:
            raise AuthenticationFailed("User doesn't exist. %s" % e)

        except Exception as e:
            raise e

        finally:
            return (user, None)
