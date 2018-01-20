from django.contrib import admin
from .models import Post

# PostModelAdmin, upgrade the view Dajngoadmin for default
class PostModelAdmin(admin.ModelAdmin):

	list_display = ['title', 'content', 'timestamp','updated']
	list_display_links = ['updated']
	list_filter = ['timestamp']
	list_editable = ['title']
	search_fields = ['title', 'content']

admin.site.register(Post, PostModelAdmin)
