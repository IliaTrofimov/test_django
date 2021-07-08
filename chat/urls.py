from django.conf.urls import url
from django.urls import path
from . import views


app_name = 'chat'


urlpatterns = [
	path('', views.index, name='index'),
	path('<int:companion_id>/', views.dialog, name='dialog'),
	path('ban/<int:creator_id>-<int:target_id>/', views.ban, name='ban'),
	path('unban/<int:creator_id>-<int:target_id>/', views.unban, name='unban'),
	path('<int:companion_id>/reload', views.reload_messages, name='reload'),
	url(r'^api/latest-chat/(?P<companion_id>\d+)/$', views.reload_messages, name='reload_messages'),
]