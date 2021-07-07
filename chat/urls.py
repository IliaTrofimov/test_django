from django.urls import path
from . import views


app_name = 'chat'

urlpatterns = [
	path('', views.index, name='index'),
	path('<int:companion_id>/', views.dialog, name='dialog'),
	path('ban/<int:creator_id>-<int:target_id>/', views.ban, name='ban'),
	path('unban/<int:creator_id>-<int:target_id>/', views.unban, name='unban'),
]