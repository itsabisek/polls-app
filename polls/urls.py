from django.conf.urls import url
from . import views as polls_views


urlpatterns = [

    url(r'^login/$', polls_views.auth_user, name="login"),
    url(r'^register/$', polls_views.register, name="register"),

    url(r'^user/newpoll/$', polls_views.new_poll, name="new_poll"),
    url(r'^user/$', polls_views.user, name="user"),
    url(r'^user/asked/$', polls_views.user_asked, name="user_asked"),
    url(r'^user/answered/$', polls_views.user_answered, name="user_answered"),
    url(r'^user/logout/$', polls_views.logout, name="logout"),

    url(r'^all/$', polls_views.AllPollsView.as_view(), name="all_polls"),
    url(r'^$', polls_views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/detail/$', polls_views.DetailView.as_view(), name="detail"),
    url(r'^(?P<pk>[0-9]+)/results/$', polls_views.ResultsView.as_view(), name="results"),
    url(r'^(?P<question_id>[0-9]+)/vote/$', polls_views.vote, name="vote"),
]
