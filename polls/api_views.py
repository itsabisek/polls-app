"""
    api_views.py: Contains all view classes/methods that handles responses
    for various endpoints
"""

from .models import Question, Choice, Answered, User
from rest_framework import filters
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework.response import Response
from .serializers import QuestionSerializer, QuestionDetailSerializer, QuestionAnsweredDetailSerializer, QuestionDetailNoVotesSerializer
from .authentication import JSONWebTokenAuthentication
from utils import get_current_time, generate_token, authenticate_user
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
import json
import logging
import uuid

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s")
handler = logging.FileHandler('view_logs.log')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


# Returns JSON for all questions asked
class AllQuestionsView(generics.ListAPIView):

    queryset = Question.objects.all().order_by('-asked_date')
    serializer_class = QuestionSerializer
    renderer_classes = [JSONRenderer]
    filter_backends = [filters.SearchFilter]
    search_fields = ['question_text']


# Returns JSON with the question text and the choices asked
class DetailView(generics.ListAPIView):

    renderer_classes = [JSONRenderer]
    authentication_classes = [JSONWebTokenAuthentication]

    def list(self, request, pk):
        try:
            queryset = Question.objects.get(pk=pk)
            serializer = QuestionDetailNoVotesSerializer(queryset)
            if request.user is not None:
                is_answered_by_user = Answered.objects.filter(
                    user_id=request.user.id, question_id=pk)
                if len(is_answered_by_user) != 0:
                    serializer = QuestionDetailSerializer(queryset)

            return Response(serializer.data, status=200)
        except User.DoesNotExist:
            print e
            return HttpResponseNotFound("The requested resource does not exist. %s" % e)
        except AuthenticationFailed, e:
            print e
            serializer = QuestionDetailNoVotesSerializer(queryset)
            return Response(serializer.data, status=200)
        except Exception, e:
            print e
            return HttpResponseNotFound("The requested resource does not exist. %s" % e)


# Returns JSON for recent questions in the User Dashboard
class UserDashboardView(generics.ListAPIView):

    filter_backends = [filters.SearchFilter]
    search_fields = ['question_text']
    renderer_classes = [JSONRenderer]
    authentication_classes = [JSONWebTokenAuthentication]

    def list(self, request):
        try:
            answered_by_user = Answered.objects.filter(
                user_id=request.user.id).values_list('question_id')
            answered_by_user = [question[0]
                                for question in answered_by_user]
            asked_by_user = User.objects.get(
                pk=request.user.id).question_set.all().values_list('id')
            asked_by_user = [question[0] for question in asked_by_user]
            questions_to_exclude = set(answered_by_user + asked_by_user)

            qs = Question.objects.all().exclude(
                pk__in=questions_to_exclude).order_by('-asked_date')

            queryset = self.filter_queryset(qs)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = QuestionSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = QuestionSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        except Exception, e:
            print e
            return HttpResponseForbidden("The page you requested cannot be loaded as %s" % e)


# Returns JSON for all questions asked by the user
class UserAskedView(generics.ListAPIView):

    filter_backends = [filters.SearchFilter]
    search_fields = ['question_text']
    renderer_classes = [JSONRenderer]
    authentication_classes = [JSONWebTokenAuthentication]

    def list(self, request):
        try:
            qs = User.objects.get(
                pk=request.user.id).question_set.all().order_by('-asked_date')

            queryset = self.filter_queryset(qs)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = QuestionDetailSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = QuestionDetailSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        except Exception, e:
            print e
            return HttpResponseForbidden("The page you requested cannot be loaded as %s" % e)


# Returns JSON for all questions answered by the user
class UserAnsweredView(generics.ListAPIView):

    filter_backends = [filters.SearchFilter]
    search_fields = ['question_text']
    renderer_classes = [JSONRenderer]
    authentication_classes = [JSONWebTokenAuthentication]

    def list(self, request):
        try:
            answered = Answered.objects.filter(
                user_id=request.user.id).order_by('-answered_on')

            answered_question_ids = [
                question[0] for question in answered.values_list('question_id')]

            questions_data = Question.objects.filter(
                pk__in=answered_question_ids).exclude(user__id=request.user.id)

            questions_ids = [question[0]
                             for question in self.filter_queryset(questions_data).values_list('id')]

            queryset = Answered.objects.filter(
                user_id=request.user.id, question_id__in=questions_ids)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = QuestionAnsweredDetailSerializer(
                    page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = QuestionAnsweredDetailSerializer(
                queryset, many=True)
            return Response(serializer.data, status=200)
        except Exception, e:
            print e
            return HttpResponseForbidden("The page you are trying to view cannot be loaded as %s" % e)


# Function to handle voting
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote(request, pk):
    try:
        is_answered = Answered.objects.filter(
            user_id=request.user.id, question_id=pk)
        if len(is_answered) == 0:
            if len(request.POST) != 0:
                    # TODO: Validate POST data here
                post_data = request.POST['choice']
                choice_selected = post_data.strip() if isinstance(post_data, str)  \
                    else post_data
            else:
                return HttpResponse("Did not find form data in body", status=500)

            choice = Question.objects.get(
                pk=pk).choice_set.get(id=int(choice_selected))
            choice.votes += 1
            choice.save()

            answered = Answered(
                user_id=request.user.id, question_id=pk, answered_on=get_current_time())
            answered.save()

        return HttpResponseRedirect(reverse('polls:detail_api', args=(pk,)))

    except Choice.DoesNotExist:
        return HttpResponseNotFound("The selected choice was not found")

    except Exception, e:
        print e
        return HttpResponseForbidden("The page you requested cannot be loaded")


# Function to handle creation of new poll.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_poll(request):
    if request.method == "GET":
        return HttpResponseNotFound("The page you requested does not exist")

    if request.method == "POST":
        try:
            user = User.objects.get(pk=request.user.id)
            if len(request.POST) != 0:
                # TODO: Validate post data here
                poll_question = request.POST['question'].strip()
                poll_choice_1 = request.POST['choice_1'].strip()
                poll_choice_2 = request.POST['choice_2'].strip()
            else:
                return HttpResponse("Did not find form data in body", status=500)
            question = Question(question_text=poll_question,
                                asked_date=get_current_time(),
                                user=user)
            question.save()
            choice_1 = Choice(choice_text=poll_choice_1, question=question)
            choice_2 = Choice(choice_text=poll_choice_2, question=question)
            choice_1.save()
            choice_2.save()

            return HttpResponse(json.dumps({'question_id': question.id}), content_type='application/json', status=200)

        except User.DoesNotExist:
            return HttpResponseNotFound("The user doesn't exist")

        except Exception, e:
            print e
            return HttpResponseForbidden("The page you request cannot be loaded as %s " % e)


# Function to authenticate user after login form is submitted
def login_user(request):
    if request.method == "GET":
        return HttpResponseNotFound("The page you are asking for does not exist")

    if request.method == 'POST':
        try:
            if len(request.POST) != 0:
                username = request.POST['username'].strip()
                password = request.POST['password'].strip()
            else:
                return HttpResponse("Did not find form data in body", status=500)

            if username is None or password is None:
                return HttpResponseForbidden("Please provide a valid name/username/password")

            if len(username) < 4:
                return HttpResponseForbidden("The username must be atleast 4 characters")

            if len(password) < 6:
                return HttpResponseForbidden("The password be atleast 6 character")

            if " " in password or " " in username:
                return HttpResponseForbidden("The username/password is not correct")

            user = authenticate_user(username=username, password=password)
            if user is None:
                return HttpResponseForbidden("The username/password is not correct")

            token = generate_token(user.uuid)
            res = json.dumps({"AUTH_TOKEN": token, "NAME": user.name})
            return HttpResponse(res, content_type='application/json', status=200)

        except Exception, e:
            print e
            return HttpResponseForbidden("The request cannot be completed as %s" % e)


# Function to register a new user
def register_user(request):
    if request.method == "GET":
        return HttpResponseNotFound("The page you requested does not exist")

    if request.method == "POST":
        try:
            if len(request.POST) != 0:
                name = request.POST['name'].strip()
                username = request.POST['username'].strip()
                password = request.POST['password'].strip()
            else:
                return HttpResponse("Did not find form data in body", status=500)

            if name is None or username is None or password is None:
                return HttpResponseForbidden("Please provide a valid name/username/password")

            if len(username) < 4:
                return HttpResponseForbidden("The username must be atleast 4 characters")

            if len(password) < 6:
                return HttpResponseForbidden("The password be atleast 6 character")

            if " " in password or " " in username:
                return HttpResponseForbidden("The username/password cannot contain whitespace")

            user = User.objects.filter(username=username)
            if len(user) != 0:
                return HttpResponseForbidden("This username already exists")

            user = User(
                username=username, name=name, password=make_password(password), uuid=uuid.uuid4().hex)
            user.save()

            token = generate_token(user.uuid)
            res = json.dumps({"AUTH_TOKEN": token, "NAME": user.name})
            return HttpResponse(res, content_type='application/json', status=200)

        except Exception, e:
            print e
            return HttpResponseForbidden("The request cannot be completed as %s" % e)


# Function to logout a user and destroy session cookies if any
def logout_user(request):
    if request.method == "GET":
        return HttpResponseNotFound("The page you requested does not exist")

    if request.method == "POST":
        authenticator = JSONWebTokenAuthentication()
        is_auth = authenticator.authenticate(request)

        if is_auth:
            return HttpResponse({"Status": "Successfully Logged out"}, status=200)

        else:
            return HttpResponseForbidden("The page you requested cannot be loaded")
