
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from django.db.models import Q

from posts.api.permission import IsOwnerOrReadOnly
from posts.api.pagination import CustomPagination

from comments.views import Comment
from .serializers import CommentEditSerializer, CommentDetailSerializer, CommentListSerializer, create_comment_serializer

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
	queryset = Comment.objects.all()
	permission_classes = [IsAuthenticated]

	def get_serializer_class(self):
		data = self.request.data
		model_type = self.request.GET.get('type')
		slug = self.request.GET.get('slug')
		parent_id = self.request.GET.get('parent_id', None)
		return create_comment_serializer(model_type=model_type, slug=slug, parent_id=parent_id, user=self.request.user)

# CommentDetailAPIView: get each Comment's json with slug or id from endpoint, method = GET 
class CommentDetailAPIView(RetrieveAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentDetailSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

'''the mixin classes provide action methods rather
than defining the handler methods, such as .get() and .post(), directly. This allows for more flexible composition of behavior.'''
# CommentEditAPIView: use mixins for: get, retrive, delete,
class CommentEditAPIView(RetrieveAPIView, UpdateModelMixin, DestroyModelMixin):
	queryset = Comment.objects.filter(id__gte=0)
	serializer_class = CommentEditSerializer

	# def get(self, request, *args, **kwargs):
	# 	return self.retrieve(request, *args, **kwargs)

	# put: return UpdateModelMixin
	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	# delete: return DestroyModelMixin
	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


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
