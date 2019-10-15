from datetime import datetime
from .models import Question, Answered, Choice
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework import generics
from rest_framework.response import Response
from .serializers import QuestionSerializer
from django.shortcuts import render


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
    return render(request, 'polls/login.html')


# Function to render the registration page
def signup_view(request):
    return render(request, 'polls/register.html')
