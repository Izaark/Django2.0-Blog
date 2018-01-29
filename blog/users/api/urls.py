from django.urls import path
from .views import UserRegisterApiView, UserLoginApiView, UserListAPIView, UserDetailAPIView

app_name = 'users-api'

# Api's endpoints !!
urlpatterns = [
	path('', UserListAPIView.as_view(), name='users'),
	path('register/', UserRegisterApiView.as_view(), name='register'),
	path('login/', UserLoginApiView.as_view(), name='login'),
	path('<int:pk>', UserDetailAPIView.as_view(), name='detail'),


]
