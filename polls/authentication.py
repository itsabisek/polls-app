from rest_framework.exceptions import AuthenticationFailed
from rest_framework import authentication
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import jwt


class JSONWebTokenAuthentication():

    def __init__(self):
        self._SECRET_KEY = 'POLLS_APP_SECRET_KEY'
        self._TOKEN_EXPIRE_TIME = 24

    def authenticate(self, request):
        token = request.COOKIES.get['AUTH_TOKEN']
        try:
            jwt.decode(token, self._SECRET_KEY, algorithms=['HS256'])
            return True
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has a failed signature")
        except jwt.InvalidSignatureError:
            raise AuthenticationFailed("Signature of token could not be validated")

        return False

    def generate_token(self, claim):
        _expiry = datetime.utcnow() + timedelta(hours=self._TOKEN_EXPIRE_TIME)
        payload = {"exp": _expiry, 'id': claim}
        token = jwt.encode(payload, self._SECRET_KEY, algorithms=["HS256"])
        return token
