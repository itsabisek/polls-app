from .models import Question, Answered, Choice
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework.response import Response
from .serializers import QuestionSerializer, QuestionDetailSerializer, QuestionResultsSerializer
from .authentication import JSONWebTokenAuthentication
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
import json


# Returns JSON with recent questions asked
class QuestionView(generics.ListAPIView):
    queryset = Question.objects.order_by('-asked_date')[:5]
    serializer_class = QuestionSerializer
    renderer_classes = [JSONRenderer]


# Returns JSON with the question text and the choices asked
class DetailView(generics.RetrieveAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    renderer_classes = [JSONRenderer]


# Returns JSON for all questions asked
class AllQuestionsView(generics.ListAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    renderer_classes = [JSONRenderer]


# Returns JSON for recent questions in the User Dashboard
class UserDashboardView(generics.ListCreateAPIView):
    queryset = Question.objects.order_by('-asked_date')[:5]
    renderer_classes = [JSONRenderer]

    def list(self, request):
        authenticator = JSONWebTokenAuthentication()
        is_auth = authenticator.authenticate(request)
        if is_auth:
            queryset = self.get_queryset()
            serializer = QuestionSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return HttpResponseForbidden("The page you are trying to view cannot be loaded")


# Returns JSON for all questions asked by the user
class UserAskedView(generics.ListCreateAPIView):

    renderer_classes = [JSONRenderer]

    def list(self, request):
        authenticator = JSONWebTokenAuthentication()
        is_auth = authenticator.authenticate(request)
        if is_auth:
            claim = authenticator.get_claim(request)
            queryset = User.objects.get(pk=int(claim)).question_set.all()
            serializer = QuestionSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return HttpResponseForbidden("The page you are trying to view cannot be loaded")


# Returns JSON for all questions answered by the user
class UserAnsweredView(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    def list(self, request):
        authenticator = JSONWebTokenAuthentication()
        is_auth = authenticator.authenticate(request)
        if is_auth:
            claim = authenticator.get_claim(request)
            question_ids = Answered.objects.filter(user_id=int(claim)).values_list('question_id')
            question_ids = [question_id[0] for question_id in question_ids]
            queryset = Question.objects.filter(pk__in=question_ids)
            serializer = QuestionSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return HttpResponseForbidden("The page you are trying to view cannot be loaded")


# Returns JSON for the results of a poll already voted
class ResultsView(generics.ListAPIView):
    renderer_classes = [JSONRenderer]

    def list(self, request, pk):
        authenticator = JSONWebTokenAuthentication()
        is_auth = authenticator.authenticate(request)
        if is_auth:
            queryset = Question.objects.get(pk=pk).choice_set.all()
            serializer = QuestionResultsSerializer(queryset, many=True)
            return Response(serializer.data, status=200)

        else:
            return HttpResponseForbidden("The page you requested cannot be loaded")


# Function to handle voting
def vote(request, pk):
    if request.method == "GET":
        return HttpResponseNotFound("The page you requested doesn't exist")

    if request.method == "POST":
        try:
            authenticator = JSONWebTokenAuthentication()
            is_auth = authenticator.authenticate(request)
            if is_auth:
                claim = authenticator.get_claim(request)
                is_answered = Answered.objects.filter(user_id=claim, question_id=pk)
                if len(is_answered) == 0:
                    choice_selected = request.POST['choice']
                    choice = Question.objects.get(pk=pk).choice_set.get(choice_text=choice_selected)
                    choice.votes += 1
                    choice.save()

                    answered = Answered(user_id=claim, question_id=pk)
                    answered.save()

                return HttpResponseRedirect(reverse('polls:results_api', args=[pk]))

            else:
                return HttpResponseForbidden("The page you requested cannot be loaded")

        except Choice.DoesNotExist:
            return HttpResponseNotFound("The selected choice was not found")

        except Exception, e:
            print e
            return HttpResponseForbidden("The page you requested cannot be loaded")


# Function to authenticate user after login form is submitted
def login_user(request):
    if request.method == "GET":
        return HttpResponseNotFound("The page you are asking for does not exist")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = authenticate(username=username, password=password)
            if user is None:
                return HttpResponseNotFound("The username is not correct")
        except Exception, e:
            print e

        token = JSONWebTokenAuthentication().generate_token(user.id)

        return HttpResponse(json.dumps({"AUTH_TOKEN": token}), content_type='application/json', status=200)


# Function to register a new user
def register_user(request):
    if request.method == "GET":
        return HttpResponseNotFound("The page you requested does not exist")

    if request.method == "POST":
        try:
            authenticator = JSONWebTokenAuthentication()
            name = request.POST['name']
            username = request.POST['username']
            password = request.POST['password']

            user = User.objects.filter(username=username)
            if len(user) != 0:
                return HttpResponseForbidden("The user already exists")

            user = User.objects.create_user(username=username, first_name=name, password=password)
            user.save()

            token = authenticator.generate_token(claim=user.id)
            return HttpResponse(json.dumps({'AUTH_TOKEN': token}), content_type='application/json', status=200)

        except Exception, e:
            print e


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
