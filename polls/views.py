from .models import Question, Choice, Answered
from .forms import LoginForm, RegistrationForm, NewPollForm
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as logout_user, login as login_user
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

import logging

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s")
handler = logging.FileHandler('view_logs.log')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


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

    try:
        q = get_object_or_404(Question, pk=question_id)
        selected_choice = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        logger.warning("No choice was selected while voting by user-%d" % request.user.id)
        return render(request, 'polls/detail.html', {
            'question': q,
            'error_message': 'You did not select a choice'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        logger.info("User-%d has voted for question-%d" % (request.user.id, q.id))
        exists = Answered.objects.filter(user_id=request.user.id, question_id=q.id)
        if len(exists) == 0:
            logger.info("User has already voted for this question once will not update in db")
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
                logger.info("User credentials entered: username-%s" % username)
                if user is not None:
                    logger.info("User credentials has been validated for username-%s" % username)
                    logger.info("Logging in user-%d" % user.id)
                    login_user(request, user)
                    return HttpResponseRedirect(reverse('polls:user'))
                else:
                    logger.warning("User credentials could not be validated for username-%s" % username)
                    error_message = "Invalid Username/Password"
        except Exception, e:
            logger.error("Exception caught- %s" % e, exc_info=True)

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

                logger.info("Checking credentials for new username-%s" % username)
                user = User.objects.filter(username=username)

                if len(user) != 0:
                    error_message = "Username already exists! Choose a different username"
                    logger.warning("Username already exists")

                else:
                    user = User.objects.create_user(username=username, first_name=name, password=password)
                    user.save()
                    logger.info("Added username-%s to database. User Id-%d" % (username, user.id))
                    login_user(request, authenticate(username=username, password=password))
                    logger.info("Logging in user-%d" % user.id)
                    return HttpResponseRedirect(reverse('polls:user'))
        except Exception, e:
            logger.error("Caught exception: %s" % e, exc_info=True)
    else:
        form = RegistrationForm()

    context = {'form': form, 'error_message': error_message}

    return render(request, 'polls/register.html', context)


# View function to show user dashboard that shows 10 recent polls
# created by the user
@login_required
def user(request):
    try:
        questions_list = Question.objects.order_by('-asked_date')[:5]
    except Exception, e:
        logger.error("Exception caught: %s" % e, exc_info=True)

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

                logger.info("New poll started by user-%(user)d. Question id-%(question)d" %
                            {'user': request.user.id, 'question': question.id})

                return HttpResponseRedirect(reverse('polls:user'))
        except Exception, e:
            logger.error("Exception caught: %s" % e, exc_info=True)
    else:
        form = NewPollForm()

    return render(request, 'polls/new_poll.html', {'form': form})


# View function to show all polls created by the user
@login_required
def user_asked(request):
    try:
        questions_list = get_object_or_404(User, pk=request.user.id).question_set.all()
        logger.info("User-%d has asked %d polls" % (request.user.id, len(questions_list)))
        context = {'questions_list': questions_list}
        return render(request, 'polls/user_asked.html', context=context)
    except Exception, e:
        logger.error("Exception caught- %s" % e, exc_info=True)


# View function that shows all polls that the user has answered
@login_required
def user_answered(request):
    try:
        question_ids = Answered.objects.filter(user_id=request.user.id).values_list('question_id')
        question_ids = [question_id[0] for question_id in question_ids]
        questions_list = Question.objects.filter(pk__in=question_ids)
        logger.info("User-%d has voted for %d polls" % (request.user.id, len(question_ids)))
        context = {'questions_list': questions_list}
        return render(request, 'polls/user_answered.html', context)
    except Exception, e:
        logger.error("Exception caught- %s" % e, exc_info=True)


# Function to logout current user and redirecting to home page
@login_required
def logout(request):
    try:
        logger.info("Logging out user-%d" % request.user.id)
        logout_user(request)
        return HttpResponseRedirect(reverse('polls:index'))
    except Exception, e:
        logger.error("Exception caught- %s" % e, exc_info=True)
