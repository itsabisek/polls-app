"""

    authentication.py: Handles the authentication and session management using JSON Web Tokens.
    Contains helper methods to create token, validate token and retrievig the payload of a token

"""


from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timedelta
import jwt
from functools import wraps


# Base class containing all the helper methods
class JSONWebTokenAuthentication():

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


# def auth_required(route_func):
#     @wraps
#     def authenticated_route_function(self, request, *args, **kwargs):
#         try:
#             authenticator = JSONWebTokenAuthentication()
#             is_auth = authenticator.authenticate(request)
#             if is_auth:
#                 claim = authenticator.get_claim(request)
#                 route_func(self, request, *args, claim=claim, **kwargs)
#             else:
#                 pass
