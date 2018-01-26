from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend

# from rest_framework.response import Response
# from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from django.db.models import Q

from posts.views import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer
from .permission import IsOwnerOrReadOnly
from .pagination import PostLimitOffSetPagination, PostPageNumberPagination, CustomPagination

# CRUD API REST

# PostListAPIView: get all Posts, method = GET
class PostListAPIView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer
	# permission_classes = [AllowAny]
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['id', 'title' ,'user__first_name','user__username']
	pagination_class = CustomPagination

	# get_queryset: get param q form uri
	def get_queryset(self, *args, **kwargs):
		# queryset_list = super(PostListAPIview, self).get_queryset(*args, **kwargs)
		queryset = Post.objects.all()
		query = self.request.GET.get('q')
		if query:
			queryset = queryset.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(user__first_name__icontains=query)).distinct()
		return queryset

# PostCreateAPIView: create  a new post from rest framework, only if user Is Authenticated, method = POST
class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsAuthenticated]

	# perform_create: save user from request (It would be not necessary) 
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

# IsAuthenticated: get each post's json with slug or id from endpoint, method = GET 
class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
  
# PostUpdateAPIView: update post's json with slug from endpoint(slug generate aut. by fun create_slug into posts.models) method = PUT
class PostUpdateAPIView(RetrieveUpdateAPIView):
	# RetrieveUpdateAPIView or UpdateAPIVie, but with UpdateAPIVie, IsOwnerOrReadOnly doesn't work
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = 'slug'
	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
	# permission_classes if the user isn't auth only read, and only can update if is owner's post(IsOwnerOrReadOnly)

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)

# PostDeleteAPIView: delete post's json with slug from endpoint, method = DELETE
class PostDeleteAPIView(RetrieveDestroyAPIView):
	# RetrieveDestroyAPIView or DestroyAPIView, but with DestroyAPIView, IsOwnerOrReadOnly doesn't work
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	# permission_classes if the user isn't auth only read, and only can delete if is owner's post(IsOwnerOrReadOnly)
	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# PostDetailUpdateDeleteAPIView: only AdminUser can use this class !!  method = [GET, PUT and DELETE]
class PostDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	permission_classes = [IsAdminUser]


# post_list: list posts with functions, is like flask !
@api_view(['GET'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


