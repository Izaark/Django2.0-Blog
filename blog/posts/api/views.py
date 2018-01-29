from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.decorators import api_view
from rest_framework.request import Request
from django.db.models import Q

from posts.views import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer
from .permission import IsOwnerOrReadOnly
from .pagination import PostLimitOffSetPagination, PostPageNumberPagination, CustomPagination

''' CRUD API REST 
The Generic views provided by REST framework allow you to quickly build API views that map closely to your database models.''' 

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
	pagination_class = CustomPagination

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

# PostDetailAPIView: get each post's json with slug or id from endpoint, method = GET 
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
	pagination_class = CustomPagination

''' The APIView class for working with class-based views '''

# post_list: list posts with functions, is like flask !
@api_view(['GET'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# post_create: create post with api view, it have more controll !!
@api_view(['POST'])
def post_create(request, *args, **kwargs):
	if request.method == 'POST':
		query = request.data
		print(query)
		serializer = PostCreateUpdateSerializer(data= query)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	return Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# post_detail: retrive and put post by slug, it have more controll !
@api_view(['GET', 'PUT'])
def post_detail(request, slug):
	try:
		post = Post.objects.get(slug=slug)
	except Post.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = PostDetailSerializer(post)
		return Response(serializer.data)

	elif request.method == 'PUT':
		serializer = PostDetailSerializer(post, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	return Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)


