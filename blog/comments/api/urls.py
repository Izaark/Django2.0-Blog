from django.urls import path
from .views import CommentListAPIView, CommentUpdateAPIView, CommentEditAPIView, CommentDetailAPIView, CommentDeleteAPIView, CommentCreateAPIView

app_name = 'comments-api'

# Api's endpoints !!
urlpatterns = [
	path('', CommentListAPIView.as_view(), name='list'),
	path('edit/<int:pk>/', CommentEditAPIView.as_view(), name='edit'),
	path('create/', CommentCreateAPIView.as_view(), name='create'),
	path('<int:pk>/', CommentDetailAPIView.as_view(), name='thread'),
	path('update/<slug:slug>/', CommentUpdateAPIView.as_view(), name='update'),
	path('delete/<slug:slug>/', CommentDeleteAPIView.as_view(), name='delete'),

]
