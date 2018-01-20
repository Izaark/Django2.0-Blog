from django.contrib import admin
from .models import Comment
class CommentModelAdmin(admin.ModelAdmin):

	list_display = ['user','timestamp','content']
	list_display_links = ['timestamp']
	list_filter = ['timestamp']
	list_editable = ['content']
	search_fields = ['user', 'content']

admin.site.register(Comment, CommentModelAdmin)
