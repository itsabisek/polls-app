from django.conf.urls import url, include
from . import views as polls_views
from . import api_views
# from rest_framework import routers

urlpatterns = [

    url(r'^login/$', api_views.login_view, name="login"),
    url(r'^register/$', api_views.signup_view, name="register"),
    #
    url(r'^user/newpoll/$', polls_views.new_poll, name="new_poll"),
    url(r'^user/$', api_views.user, name="user"),
    url(r'^user/asked/$', polls_views.user_asked, name="user_asked"),
    url(r'^user/answered/$', polls_views.user_answered, name="user_answered"),
    # url(r'^user/logout/$', polls_views.logout, name="logout"),
    #
    # url(r'^all/$', polls_views.AllPollsView.as_view(), name="all_polls"),
    # url(r'^$', polls_views.IndexView.as_view(), name='index'),
    # url(r'^(?P<pk>[0-9]+)/detail/$', polls_views.DetailView.as_view(), name="detail"),
    # url(r'^(?P<pk>[0-9]+)/results/$', polls_views.ResultsView.as_view(), name="results"),
    url(r'^(?P<question_id>[0-9]+)/vote/$', polls_views.vote, name="vote"),

    url(r'^$', api_views.QuestionView.as_view(), name="index"),
    url(r'^api/detail/(?P<pk>[0-9]+)/$', api_views.DetailView.as_view(), name="detail"),
    url(r'^api/all/$', api_views.AllQuestionsView.as_view(), name="all_polls"),
    url(r'^api/login$', api_views.login_user, name="login_api"),
    url(r'^api/register', api_views.register_user, name="register_api"),
    url(r'^api/logout', api_views.logout_user, name="logout_api")
]
