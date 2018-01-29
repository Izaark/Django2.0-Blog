from django.contrib import admin
from django.urls import path, include
from posts import views
from django.conf import settings
from django.conf.urls.static import static
from users.views import login_view, logout_view, register_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls', namespace='posts')),

    path('comments/', include('comments.urls', namespace='comments')),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    # api restframework !
    path('api/posts/', include('posts.api.urls', namespace='posts-api')),
    path('api/comments/', include('comments.api.urls', namespace='comments-api')),
    path('api/users/', include('users.api.urls', namespace='users-api')),
]
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)