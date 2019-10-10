from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from .models import Question, Choice, Answered
# from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as logout_user, login as login_user
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .forms import LoginForm, RegistrationForm, NewPollForm
from datetime import datetime


# Generic View class for index page
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'questions_list'

    def get_queryset(self):
        return Question.objects.order_by('-asked_date')[:5]


# Generic View class for all polls
class AllPollsView(generic.ListView):
    template_name = 'polls/all_polls.html'
    context_object_name = 'questions_list'

    def get_queryset(self):
        return Question.objects.all().order_by('-asked_date')


# Generic view class for details of individual poll and to vote for it
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DetailView, self).dispatch(*args, **kwargs)


# Generic view class for showing votes each choice of a poll has received
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResultsView, self).dispatch(*args, **kwargs)


# Function to accept POST request from voting page and redirect to results page
# after updating vote in database
def vote(request, question_id):
    q = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': q,
            'error_message': 'You did not select a choice'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        exists = Answered.objects.filter(user_id=request.user.id, question_id=q.id)
        if len(exists) == 0:
            answered = Answered(user_id=request.user.id, question_id=q.id)
            answered.save()

    return HttpResponseRedirect(reverse('polls:results', args=(q.id,)))


# Function to handle login of user
def auth_user(request):
    error_message = ""
    if request.method == 'POST':
        try:
            form = LoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(username=username, password=password)

                if user is not None:
                    login_user(request, user)
                    return HttpResponseRedirect(reverse('polls:user'))
                else:
                    error_message = "Invalid Username/Password"
        except Exception, e:
            print "Exception- ", e
    else:
        form = LoginForm()

    context = {'form': form, 'error_message': error_message}

    return render(request, 'polls/login.html', context)


# Funtion to handle registration of new user
def register(request):
    error_message = ""
    if request.method == 'POST':
        try:
            form = RegistrationForm(request.POST)

            if form.is_valid():
                name = request.POST['name']
                username = request.POST['username']
                password = request.POST['password']

                user = User.objects.filter(username=username)

                if len(user) != 0:
                    error_message = "Username already exists! Choose a different username"

                else:
                    user = User.objects.create_user(username=username, first_name=name, password=password)
                    user.save()
                    login_user(request, authenticate(username=username, password=password))
                    return HttpResponseRedirect(reverse('polls:user'))
        except Exception, e:
            print "Exception Caught: ", e
    else:
        form = RegistrationForm()

    context = {'form': form, 'error_message': error_message}

    return render(request, 'polls/register.html', context)


# View function to show user dashboard that shows 10 recent polls
# created by the user
@login_required
def user(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    try:
        questions_list = Question.objects.order_by('-asked_date')[:5]
    except Exception, e:
        print "Exception Caught: ", e
    context = {"questions_list": questions_list}

    return render(request, 'polls/user.html', context=context)


# View to show new poll page for a user and accept POST requests
# from the new poll page and updating to database
@login_required
def new_poll(request):

    if request.method == 'POST':
        try:
            form = NewPollForm(request.POST)

            if form.is_valid():
                question = request.POST['question']
                choice_one = request.POST['choice_one']
                choice_two = request.POST['choice_two']

                question = Question(user=request.user, question_text=question, asked_date=datetime.now())
                question.save()

                choice_1 = Choice(choice_text=choice_one, question=question)
                choice_2 = Choice(choice_text=choice_two, question=question)
                choice_1.save()
                choice_2.save()

                return HttpResponseRedirect(reverse('polls:user'))
        except Exception, e:
            print "Exception Caught: ", e
    else:
        form = NewPollForm()

    return render(request, 'polls/new_poll.html', {'form': form})


# View function to show all polls created by the user
@login_required
def user_asked(request):
    questions_list = get_object_or_404(User, pk=request.user.id).question_set.all()
    context = {'questions_list': questions_list}
    return render(request, 'polls/user_asked.html', context=context)


# Function to logout current user and redirecting to home page
@login_required
def logout(request):
    try:
        logout_user(request)
    except Exception, e:
        print "Exception caught: ", e
    return HttpResponseRedirect(reverse('polls:index'))


# View function that shows all polls that the user has answered
@login_required
def user_answered(request):
    try:
        question_ids = Answered.objects.filter(user_id=request.user.id).values_list('question_id')
        question_ids = [question_id[0] for question_id in question_ids]
        questions_list = Question.objects.filter(pk__in=question_ids)
        context = {'questions_list': questions_list}
        return render(request, 'polls/user_answered.html', context)
    except Exception, e:
        print "Exception caught- ", e
