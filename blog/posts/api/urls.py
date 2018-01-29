from django.urls import path
from .views import PostListAPIView, PostDetailAPIView, PostUpdateAPIView, PostDeleteAPIView, PostCreateAPIView, PostDetailUpdateDeleteAPIView, post_list, post_create, post_detail

app_name = 'posts-api'

# Api's endpoints !!
urlpatterns = [
	path('', PostListAPIView.as_view(), name='list'),
	path('create/', PostCreateAPIView.as_view(), name='create'),
	path('<slug:slug>/', PostDetailAPIView.as_view(), name='detail'),
	path('update/<slug:slug>/', PostUpdateAPIView.as_view(), name='update'),
	path('delete/<slug:slug>/', PostDeleteAPIView.as_view(), name='delete'),
	path('update/delete/<slug:slug>/', PostDetailUpdateDeleteAPIView.as_view(), name='create-delete'),
	# api views
	path('list/', post_list, name='view-list'),
	path('create/view/', post_create, name='view-create'),
	path('<slug:slug>/detail/', post_detail, name='view-detail'),

]