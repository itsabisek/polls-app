from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic


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


def login(request):
    pass


def register(request):
    pass


def user(request):
    pass


def new_poll(request):
    pass


def user_asked(request):
    pass


def user_answered(request):
    pass


def user_asked(request):
    pass


def logout(request):
    pass


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
