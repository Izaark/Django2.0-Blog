from django.contrib import admin
from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('create/', views.create, name='create'),
    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('<slug:slug>/update/', views.update, name='update'),
    path('<slug:slug>/delete/', views.delete, name='delete'),
    path('', views.list, name='list'),
    path('list/', views.PostListView.as_view(), name='list-view'),
    
]
