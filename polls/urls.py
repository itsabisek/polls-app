from django.conf.urls import url
from . import api_views

urlpatterns = [

    url(r'^api/detail/(?P<pk>[0-9]+)/$', api_views.DetailView.as_view(), name="detail_api"),
    url(r'^api/all/$', api_views.AllQuestionsView.as_view(), name="all_polls"),
    url(r'^api/user/$', api_views.UserDashboardView.as_view(), name="user_dashboard"),
    url(r'^api/user/asked/$', api_views.UserAskedView.as_view(), name="user_asked"),
    url(r'^api/user/answered/$', api_views.UserAnsweredView.as_view(), name="user_answered"),
    url(r'^api/user/new/$', api_views.new_poll, name="new_poll"),
    url(r'^api/vote/(?P<pk>[0-9]+)/$', api_views.vote, name="vote"),
    url(r'^api/login$', api_views.login_user, name="login_api"),
    url(r'^api/register/$', api_views.register_user, name="register_api"),
    url(r'^api/logout/$', api_views.logout_user, name="logout_api")
]
