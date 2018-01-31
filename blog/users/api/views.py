
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

from posts.api.permission import IsOwnerOrReadOnly
from posts.api.pagination import CustomPagination

from .serializers import UserRegisterSerializer, UserLiginSerializer, UserListSerializer, UserDetailSerializer
from rest_framework_jwt.settings import api_settings

User = get_user_model()

# UserDetailAPIView: get each user's json with id from endpoint, method = GET 
class UserDetailAPIView(RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserDetailSerializer
	# lookup_field = 'username'
	permission_class = [IsAdminUser]

# UserListAPIView: Get all users ! method = GET 
class UserListAPIView(ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserListSerializer
	permission_class = [IsAdminUser]
	pagination_class = CustomPagination

# UserRegisterApiView: Register a new user method = POST 
class UserRegisterApiView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserRegisterSerializer
	permission_class = [AllowAny]

# Using the APIView class is pretty much the same as using a regular View class, as usual
# UserLoginApiView: login user with APIView is like view !  method = POST 
class UserLoginApiView(APIView):
	serializer_class = UserLiginSerializer
	permission_class = [AllowAny]

	# post get data from client and pass to UserLiginSerializer
	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = UserLiginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			return Response(new_data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)