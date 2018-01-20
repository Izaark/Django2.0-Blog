from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.views.generic  import ListView, CreateView, UpdateView, DeleteView

#create a new posts method=POST
def create(request):
	# if not request.user.is_staff or not  request.user.is_superuser: #if user dont is super user or star raise http error
	# 	raise Http404

	form = PostForm(request.POST or None, request.FILES or None)

	if request.method == 'POST':
		# print (request.POST.get('title'))
		# print (request.POST.get('content'))
		pass

	if form.is_valid() and request.user.is_authenticated():
		instance = form.save(commit=False)#Dont save the post for : commit=False)
		instance.user = request.user
		#more code, change code like modidy content etc..
		instance.save()#save data
		messages.success(request, 'Post created.')
		return HttpResponseRedirect(instance.get_absolute_urlf())#
	context = {
		'form':form
	}
	return render(request, 'post_create.html', context)

#get all posts method=GET
def detail(request, slug):
	#queryset = Post.objects.all()
	obj_post = get_object_or_404(Post, slug=slug)
	#todo: fix timezone
	if obj_post.publish > timezone.now().date() or obj_post.draft :
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404

	'''get comments like comments.model, important: could be any model in this case is Post !!!!
	content_type = ContentType.objects.get_for_model(Post)
	obj_id = obj_post.id #is like Post.objets.get(id=obj_post.id)'''

	# initial_data: get data Model and id from Post
	initial_data = {
		'content_type': obj_post.get_content_type,
		'object_id': obj_post.id,
	}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		# !what happend her !! TODO: Fix this is the correct

		# c_type = form.cleaned_data.get('content_type')
		# print(c_type)
		#content_type = ContentType.objects.get(model='Post')
		content_type = ContentType.objects.get_for_model(Post)
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
	'''Get .models form app comments, into models is: Comment.objects.filter_by_instance, was create myself!! 
	comments = Comment.objects.filter_by_instance(obj_post)'''

	#upgrade to property in Post models
	comments = obj_post.comments

	#send context to html file
	context = { 
	'title': obj_post.title,
	'obj_post': obj_post,
	'comments': comments,
	'comment_form': form,
	}
	return render(request, 'post_detail.html', context)

#list all posts method=GET
def list(request):
	queryset = Post.objects.active()#This funcion was generate with models manager it's better being that have more control !!, 
	today = timezone.now().date()
	if request.user.is_staff or request.user.is_superuser:
		queryset = Post.objects.all()
	# for conten in queryset:
	# 	print(conten.image)

	#get param q from template form, and if the query have title, content or userfirstname, the qeryset it's equals to filter below
	query = request.GET.get('q')
	if query:
		queryset = queryset.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(user__first_name__icontains=query))

	#pagination !
	paginator = Paginator(queryset, 3) # Show 3 posts per page
	page = request.GET.get('page')
	queryset = paginator.get_page(page)

	context = { 'obj_post': queryset, 'today':today}
	return render(request, 'post_list.html', context)

#update Posts method=PUT but is POST !?
def update(request, slug):	
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)	#first get all data in model Post with slug from url

	'''this form is equal to intance and request.POST or None,
		for get the method post and quit the automatic message'''
	form = PostForm(request.POST or None,request.FILES or None, instance= instance)
	if form.is_valid():
		instance = form.save(commit=False)#dont save yet !
		instance.save()
		messages.success(request, 'Post details updated.')
		return HttpResponseRedirect(instance.get_absolute_urlf())#redirect to post detail whit id

	context = {
		'title': instance.title,
		'content': instance.content,
		'form': form
	}
	return render(request, 'post_update.html', context)#render all context in hmtl file

#delete Posts method=DELETE
def delete(request, slug):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, 'Post was deleted')
	return redirect('posts:list')

# base in class views , is more fastes
class PostListView(ListView):
	model = Post
	template_name = "post_list.html"

