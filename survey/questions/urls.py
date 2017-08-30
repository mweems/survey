from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
	url(r'^adminPage/$', views.adminPage, name='adminPage'),
    url(r'^delete_question/$', views.deleteQuestion, name='deleteQuestion'),
    url(r'^add_question/$', views.addQuestion, name='addQuestion'),
    url(r'^add_choice/$', views.addChoice, name='addChoice'),
    url(r'^delete_choice/$', views.deleteChoice, name='deleteChoice'),
    url(r'^login/$', views.myLogin, name='login'),
]