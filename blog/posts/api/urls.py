from django.urls import path
from .views import PostListAPIView, PostDetailAPIView, PostUpdateAPIView, PostDeleteAPIView, PostCreateAPIView, PostDetailUpdateDeleteAPIView, post_list

app_name = 'posts-api'

# Api's endpoints !!
urlpatterns = [
	path('', PostListAPIView.as_view(), name='list'),
	path('list/', post_list, name='post-list'),
	path('create/', PostCreateAPIView.as_view(), name='create'),
	path('<slug:slug>/', PostDetailAPIView.as_view(), name='detail'),
	# path('<int:pk>/', PostDetailAPIView.as_view(), name='api-posts-list'),
	path('<slug:slug>/update', PostUpdateAPIView.as_view(), name='update'),
	path('<slug:slug>/delete', PostDeleteAPIView.as_view(), name='delete'),
	path('<slug:slug>/update/delete', PostDetailUpdateDeleteAPIView.as_view(), name='create-delete'),

]