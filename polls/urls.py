from django.conf.urls import url
from . import views as polls_views
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', polls_views.DetailView.as_view(), name="detail"),
    url(r'^$', polls_views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/results/$', polls_views.ResultsView.as_view(), name="results"),
    url(r'^(?P<question_id>[0-9]+)/vote/$', polls_views.vote, name="vote"),
    url(r'^login/$', login, name='login')
]
