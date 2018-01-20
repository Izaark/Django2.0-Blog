from django.contrib import admin
from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [
	path('<int:id>/', views.comment_thread, name='detail'),
	path('<int:id>/delete', views.comment_delete, name='delete'),
	path('<int:pk>/delete/view', views.CommentDeleteView.as_view(), name='delete-view'),
	
]
