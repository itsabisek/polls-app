import jwt
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from models import User
from django.contrib.auth.hashers import make_password, check_password


# Base class containing all the helper methods
def authenticate_token(request):
    """
        Method to vaidate a token in the request headers. Raises an exception if token
        is not found in request header, invalid token or expired token

    """

    try:
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[-1]
        jwt.decode(token, settings.KEY, algorithms=['HS256'])
        return True
    except KeyError:
        raise AuthenticationFailed("Token not found in header")
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has an expired signature")
    except jwt.InvalidSignatureError:
        raise AuthenticationFailed(
            "Signature of token could not be validated")

    return False


def generate_token(claim):
    """
        Generates a token with the claim as the payload. The token will be valid for
        24 hours by default

    """

    _expiry = datetime.utcnow() + timedelta(hours=settings.TOKEN_EXPIRE_TIME)
    payload = {"exp": _expiry, 'id': claim}
    token = jwt.encode(payload, settings.KEY, algorithm="HS256")
    return token


def get_token_payload(request):
    """
        Returns the payload inside the token in the request. Raises an exception if 
        token is not found in the request headers
    """
    try:
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[-1]
        return jwt.decode(token, settings.KEY, algorithms=['HS256']).get('id')
    except KeyError:
        raise AuthenticationFailed("Token not found in header")


def authenticate_user(username=None, password=None):
    """
        Authenticates the user by checking if the username/password matches.
        Uses django's built in function to handle password hashing so no need to
        encrypt the password manually and uses salted hashing.
        returns the user instance if available else None

    """
    if username is None or password is None:
        return None
    try:
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            return user
        return None
    except User.DoesNotExist:
        return None


def get_current_time():
    """
        Returns the current datetime with appropriate timezone information

    """
    return datetime.now(tz=timezone.get_default_timezone())
