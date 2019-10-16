from datetime import datetime
from .models import Question, Answered, Choice
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework import generics
from rest_framework.response import Response
from .serializers import QuestionSerializer
from django.shortcuts import render
from .authentication import JSONWebTokenAuthentication
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Renders a view with list of recent polls. (Equivalent to index page)
class QuestionView(generics.ListAPIView):

    queryset = Question.objects.order_by('-asked_date')[:5]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, format=None):
        self.questions = self.get_queryset()
        return Response({'questions_list': self.questions}, template_name='polls/index.html')


# Renders a view with detail of each question
class DetailView(generics.RetrieveAPIView):
    queryset = Question.objects.all()

    def get(self, request, pk, format=None):
        self.object = self.get_object()
        return Response({'question': self.object}, template_name='polls/detail.html')


# Renders a view which lists all polls
class AllQuestionsView(generics.ListAPIView):
    queryset = Question.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, format=None):
        self.questions = self.get_queryset()
        return Response({'questions_list': self.questions}, template_name='polls/all_polls.html')


# Renders user dashboard
class UserDashboardView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, format=None):
        pass


# Function to render a login forms
def login_view(request):
    authenticator = JSONWebTokenAuthentication()
    is_auth = authenticator.authenticate(request)
    if not is_auth:
        return render(request, 'polls/login.html')

    return HttpResponseRedirect(reverse('polls:user'))


# Function to render the registration page
def signup_view(request):
    return render(request, 'polls/register.html')


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

        response = HttpResponseRedirect(reverse('polls:user'))
        response.set_cookie('AUTH_TOKEN', token)
        return response


def user(request):

    authenticator = JSONWebTokenAuthentication()
    is_auth = authenticator.authenticate(request)

    if is_auth:
        print "Authenticated"
        try:
            questions_list = Question.objects.order_by('-asked_date')[:5]
        except Exception, e:
            print e

        context = {"questions_list": questions_list}
        return render(request, 'polls/user.html', context=context)
    else:
        return HttpResponseRedirect(reverse('polls:login'))


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
                return HttpResponseNotFound("The user already exists")

            user = User.objects.create_user(username=username, first_name=name, password=password)
            user.save()

            token = authenticator.generate_token(claim=user.id)
            response = HttpResponseRedirect(reverse('polls:user'))
            response.set_cookie('AUTH_TOKEN', token)
            return response

        except Exception, e:
            print e


# Function to logout a user and destroy session cookies if any
def logout_user(request):
    authenticator = JSONWebTokenAuthentication()
    is_auth = authenticator.authenticate(request)

    if is_auth:
        response = HttpResponseRedirect(reverse('polls:index'))
        response.delete_cookie('AUTH_TOKEN')

    else:
        response = HttpResponseRedirect(reverse('polls:index'))

    return response
