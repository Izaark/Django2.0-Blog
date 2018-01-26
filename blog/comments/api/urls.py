from django.urls import path
from .views import CommentListAPIView, CommentDetailAPIView, CommentUpdateAPIView, CommentDeleteAPIView, CommentCreateAPIView

app_name = 'comments-api'

# Api's endpoints !!
urlpatterns = [
	path('', CommentListAPIView.as_view(), name='list'),
	path('create/', CommentCreateAPIView.as_view(), name='create'),
	path('<int:pk>/', CommentDetailAPIView.as_view(), name='thread'),
	path('<slug:slug>/update', CommentUpdateAPIView.as_view(), name='update'),
	path('<slug:slug>/delete', CommentDeleteAPIView.as_view(), name='delete'),

]
