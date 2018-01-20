from django.shortcuts import render, get_object_or_404
from .models import Comment
from .forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect,Http404, HttpResponse
from posts.models import Post
from django.contrib import messages
from django.views.generic  import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
# Create your views here

# comment_thread, get treads from comment parent
@login_required()
def comment_thread(request, id):
	try:
		obj = get_object_or_404(Comment, id=id)
	except:
		raise Http404

	# TODO: FIX content_type relashion !
	# if not obj.is_parent:
	# 	obj = obj.parent

	initial_data = {
		'content_type': obj.content_type,
		'object_id': obj.id,
	}

	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		#TODO: Fix This wtf
		# c_type = form.cleaned_data.get('content_type')
		# print(c_type)
		# content_type = ContentType.objects.get(model='Post')
		content_type = ContentType.objects.get_for_model(Comment)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get('content')

		# children comments, het id parent comment and filter the id whit id parent,
		parent_obj = None
		try:
			parent_id = int(request.POST.get('parent_id'))
		except:
			parent_id = None		
		if parent_id:	
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first() #get the first element comment

		# crate new comment whit the same paramhs
		new_comment, created = Comment.objects.get_or_create(
							user=request.user,
							content_type=content_type,
							object_id = obj_id,
							content=content_data,
							parent= parent_obj,
			)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_urlf())
	context = {
		'comment': obj,
		'form': form,
	}

	return render(request, 'comment_thread.html', context)

# comment_delete whit param id, redirect to post's commment !
def comment_delete(request, id):
	try:
		obj = get_object_or_404(Comment, id=id)
	except:
		raise Http404
	
	if obj.user != request.user:
		response = HttpResponse('No tienes permiso para eliminar este comentario')
		response.status_code = 403
		return response
	if request.method == "POST":

		# url from post :D fix it !?  example/posts/detail/btc/
		url_obj_parent = obj.content_object.get_absolute_urlf()
		obj.delete()
		messages.success(request, 'deleted !!!')
		return HttpResponseRedirect(url_obj_parent)

	context = {
		'object': obj,
	}
	return render(request, 'comment_delete.html', context)

# CommentDeleteView
class CommentDeleteView(DeleteView):
	model = Comment
	template_name = 'comment_delete.html'
