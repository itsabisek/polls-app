"""
    api_views.py: Contains all view classes/methods that handles responses
    for various endpoints
"""

from .models import Question, Answered, Choice
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework.response import Response
from .serializers import QuestionSerializer, QuestionDetailSerializer, QuestionAnsweredDetailSerializer, QuestionDetailNoVotesSerializer
from .authentication import JSONWebTokenAuthentication
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.utils import timezone
import json


# Returns JSON for all questions asked
class AllQuestionsView(generics.ListAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    renderer_classes = [JSONRenderer]


# Returns JSON with the question text and the choices asked
class DetailView(generics.ListAPIView):

    renderer_classes = [JSONRenderer]

    def list(self, request, pk):
        try:
            queryset = Question.objects.get(pk=pk)
            serializer = QuestionDetailNoVotesSerializer(queryset)
            authenticator = JSONWebTokenAuthentication()
            is_auth = authenticator.authenticate(request)
            if is_auth:
                claim = authenticator.get_claim(request)
                is_answered_by_user = Answered.objects.filter(
                    user_id=claim, question_id=pk)
                if len(is_answered_by_user) != 0:
                    serializer = QuestionDetailSerializer(queryset)

            return Response(serializer.data, status=200)
        except AuthenticationFailed, e:
            print e
            serializer = QuestionDetailNoVotesSerializer(queryset)
            return Response(serializer.data, status=200)
        except Exception, e:
            print e
            return HttpResponseNotFound("The requested resource does not exist. %s" % e)


# Returns JSON for recent questions in the User Dashboard
class UserDashboardView(generics.ListAPIView):
    renderer_classes = [JSONRenderer]

    def list(self, request):
        try:
            authenticator = JSONWebTokenAuthentication()
            is_auth = authenticator.authenticate(request)
            if is_auth:
                claim = authenticator.get_claim(request)
                answered_by_user = Answered.objects.filter(
                    user_id=claim).values_list('question_id')
                answered_by_user = [question[0]
                                    for question in answered_by_user]
                asked_by_user = User.objects.get(
                    pk=claim).question_set.all().values_list('id')
                asked_by_user = [question[0] for question in asked_by_user]
                questions_to_exclude = set(answered_by_user + asked_by_user)

                queryset = Question.objects.all().exclude(pk__in=questions_to_exclude)
                serializer = QuestionSerializer(queryset, many=True)
                return Response(serializer.data, status=200)
            else:
                return HttpResponseForbidden("The page you are trying to view cannot be loaded")
        except Exception, e:
            print e
            return HttpResponseForbidden("The page you requested cannot be loaded as %s" % e)


# Returns JSON for all questions asked by the user
class UserAskedView(generics.ListAPIView):

    renderer_classes = [JSONRenderer]

    def list(self, request):
        authenticator = JSONWebTokenAuthentication()
        is_auth = authenticator.authenticate(request)
        if is_auth:
            claim = authenticator.get_claim(request)
            queryset = User.objects.get(pk=int(claim)).question_set.all()
            serializer = QuestionDetailSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return HttpResponseForbidden("The page you are trying to view cannot be loaded")


# Returns JSON for all questions answered by the user
class UserAnsweredView(generics.ListAPIView):
    renderer_classes = [JSONRenderer]

    def list(self, request):
        authenticator = JSONWebTokenAuthentication()
        is_auth = authenticator.authenticate(request)
        if is_auth:
            claim = authenticator.get_claim(request)
            queryset = Answered.objects.filter(user_id=int(claim))
            serializer = QuestionAnsweredDetailSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return HttpResponseForbidden("The page you are trying to view cannot be loaded")


# Function to handle voting
def vote(request, pk):
    if request.method == "GET":
        return HttpResponseNotFound("The page you are asking for does not exist")

    if request.method == 'POST':
        try:
            authenticator = JSONWebTokenAuthentication()
            is_auth = authenticator.authenticate(request)
            if is_auth:
                claim = authenticator.get_claim(request)
                is_answered = Answered.objects.filter(
                    user_id=claim, question_id=pk)
                if len(is_answered) == 0:
                    if len(request.POST) != 0:
                        # TODO: Validate POST data here
                        post_data = request.POST['choice']
                        choice_selected = post_data.strip() if isinstance(post_data, str)  \
                            else post_data
                    else:
                        # TODO: Validate request body here
                        data = json.loads(request.body.decode('utf-8'))
                        choice_selected = data['choice'].strip() if isinstance(data['choice'], str)  \
                            else data['choice']

                    choice = Question.objects.get(
                        pk=pk).choice_set.get(id=int(choice_selected))
                    choice.votes += 1
                    choice.save()

                    answered = Answered(
                        user_id=claim, question_id=pk, answered_on=timezone.now())
                    answered.save()

                return HttpResponseRedirect(reverse('polls:detail_api', args=(pk,)))

            else:
                return HttpResponseForbidden("The page you requested cannot be loaded")

        except Choice.DoesNotExist:
            return HttpResponseNotFound("The selected choice was not found")

        except Exception, e:
            print e
            return HttpResponseForbidden("The page you requested cannot be loaded")


# Function to handle creation of new poll.
def new_poll(request):
    if request.method == "GET":
        return HttpResponseNotFound("The page you requested does not exist")

    if request.method == "POST":
        try:
            authenticator = JSONWebTokenAuthentication()
            is_auth = authenticator.authenticate(request)
            if is_auth:
                claim = authenticator.get_claim(request)
                user = User.objects.get(pk=claim)
                if len(request.POST) != 0:
                    # TODO: Validate post data here
                    poll_question = request.POST['question'].strip()
                    poll_choice_1 = request.POST['choice_1'].strip()
                    poll_choice_2 = request.POST['choice_2'].strip()
                else:
                    # TODO: Validate request body here
                    data = json.loads(request.body.decode('utf-8'))
                    poll_question = data['question'].strip()
                    poll_choice_1 = data['choice_1'].strip()
                    poll_choice_2 = data['choice_2'].strip()

                question = Question(question_text=poll_question,
                                    asked_date=timezone.now(),
                                    user=user)
                question.save()
                choice_1 = Choice(choice_text=poll_choice_1, question=question)
                choice_2 = Choice(choice_text=poll_choice_2, question=question)
                choice_1.save()
                choice_2.save()

                return HttpResponse(json.dumps({'question_id': question.id}), content_type='application/json', status=200)

            else:
                return HttpResponseForbidden("The page you requested cannot be loaded")

        except User.DoesNotExist:
            return HttpResponseNotFound("The user doesn't exist")

        except Exception, e:
            print e
            return HttpResponseForbidden("The page you requested cannot be loaded")


# Function to authenticate user after login form is submitted
def login_user(request):
    if request.method == "GET":
        return HttpResponseNotFound("The page you are asking for does not exist")

    if request.method == 'POST':
        try:
            if len(request.POST) != 0:
                # TODO: Validate post data here
                username = request.POST['username'].strip()
                password = request.POST['password'].strip()
            else:
                # TODO: Validate request body here
                data = json.loads(request.body.decode('utf-8'))
                username = data['username'].strip()
                password = data['password'].strip()

            user = authenticate(username=username, password=password)
            if user is None:
                return HttpResponseForbidden("The username/password is not correct")

            token = JSONWebTokenAuthentication().generate_token(user.id)
            return HttpResponse(json.dumps({"AUTH_TOKEN": token}), content_type='application/json', status=200)

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
                # TODO: Validate Post data here
                name = request.POST['name'].strip()
                username = request.POST['username'].strip()
                password = request.POST['password'].strip()
            else:
                # TODO: Validate request body here
                data = json.loads(request.body.decode('utf-8'))
                name = data['name'].strip()
                username = data['username'].strip()
                password = data['password'].strip()

            user = User.objects.filter(username=username)
            if len(user) != 0:
                return HttpResponseForbidden("This username already exists")

            user = User.objects.create_user(
                username=username, first_name=name, password=password)
            user.save()

            return HttpResponseRedirect(reverse('polls:login_api'))

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
