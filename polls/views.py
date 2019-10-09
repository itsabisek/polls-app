from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from .models import Question, Choice
# from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as logout_user, login as login_user
from django.contrib.auth.models import User
from .forms import LoginForm, RegistrationForm, NewPollForm
from datetime import datetime


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'questions_list'

    def get_queryset(self):
        return Question.objects.order_by('-asked_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


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

    return HttpResponseRedirect(reverse('polls:results', args=(q.id,)))


def all_polls(request):
    questions_list = Question.objects.all()
    return render(request, 'polls/all_polls.html', {'questions_list': questions_list})


def auth_user(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login_user(request, user)
                return HttpResponseRedirect(reverse('polls:user'))

    else:
        form = LoginForm()

    return render(request, 'polls/login.html', {'form': form})


def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            name = request.POST['name']
            username = request.POST['username']
            password = request.POST['password']

            user = User.objects.filter(username=username)

            if len(user) != 0:
                return HttpResponseRedirect(reverse('polls:login'))

            else:
                user = User.objects.create_user(username=username, first_name=name, password=password)
                user.save()

                login_user(request, authenticate(username=username, password=password))
                return HttpResponseRedirect(reverse('polls:user'))
    else:
        form = RegistrationForm()

    return render(request, 'polls/register.html', {'form': form})


@login_required
def user(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))

    questions_list = User.objects.get(pk=request.user.id).question_set.order_by('-asked_date')[:10]
    context = {"questions_list": questions_list}

    return render(request, 'polls/user.html', context=context)


@login_required
def new_poll(request):

    if request.method == 'POST':

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

    else:
        form = NewPollForm()

    return render(request, 'polls/new_poll.html', {'form': form})


@login_required
def user_asked(request):
    questions_list = User.objects.get(pk=request.user.id).question_set.all()
    context = {'questions_list': questions_list}
    return render(request, 'polls/user_asked.html', context=context)


@login_required
def logout(request):
    logout_user(request)
    return HttpResponseRedirect(reverse('polls:index'))

#
# def user_answered(request):
#     questions_list = Question.objects.all()
#     context = {'questions_list': questions_list}
#     return render(request, 'polls/user_asked.html', context)


# def index(request):
#     questions_list = Question.objects.all()
#     context = {
#         'questions_list': questions_list,
#     }
#
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
#
#     return HttpResponse(response % question_id)
