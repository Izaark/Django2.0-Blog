
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from posts.api.permission import IsOwnerOrReadOnly
from posts.api.pagination import CustomPagination

from comments.views import Comment
from .serializers import CommentDetailSerializer, CommentListSerializer

# CRUD API REST

# CommentListAPIView: get all Comments, method = GET
class CommentListAPIView(ListAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentListSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['id', 'content', 'user__username']
	pagination_class = CustomPagination

	# get_queryset: get param q form uri
	def get_queryset(self, *args, **kwargs):
		queryset = Comment.objects.all()
		query = self.request.GET.get('q')
		if query:
			queryset = queryset.filter(Q(content__icontains=query) | Q(user__first_name__icontains=query)).distinct()
		return queryset

# CommentCreateAPIView: create  a new Comment from rest framework, only if user Is Authenticated, method = Comment
class CommentCreateAPIView(CreateAPIView):
	pass

# CommentDetailAPIView: get each Comment's json with slug or id from endpoint, method = GET 
class CommentDetailAPIView(RetrieveAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentDetailSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

# CommentUpdateAPIView: update Comment's json with slug from endpoint(slug generate aut. by fun create_slug into Comments.models) method = PUT
class CommentUpdateAPIView(RetrieveUpdateAPIView):
	pass

# CommentDeleteAPIView: delete Comment's json with slug from endpoint, method = DELETE
class CommentDeleteAPIView(RetrieveDestroyAPIView):
	# RetrieveDestroyAPIView or DestroyAPIView, but with DestroyAPIView, IsOwnerOrReadOnly doesn't work
	# queryset = Comment.objects.all()
	# serializer_class = CommentDetailSerializer
	# lookup_field = 'slug'
	# # permission_classes if the user isn't auth only read, and only can delete if is owner's Comment(IsOwnerOrReadOnly)
	# permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
	pass
