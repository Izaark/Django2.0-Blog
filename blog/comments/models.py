from django.db import models
#from posts.models import Post
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy


#CommentManager override models, add filter_by_instance function for filtering by model and id from Post.views:detail
#CommentManager its more dinamic give any model this for: instance.__class__
class CommentManager(models.Manager):

	# all only give the comments that its not parents, only childs comment
	def all(self):
		qs = super(CommentManager, self).filter(parent=None)
		return qs

	def filter_by_instance(self, instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		obj_id = instance.id
		qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
		return qs

	# create_by_model_type: create comment depends of model ! all that for GenericForeignKey
	def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
		model_qs = ContentType.objects.filter(model=model_type)
		if model_qs.exists():
			SomeModel = model_qs.first().model_class()
			obj_qs = SomeModel.objects.filter(slug=slug)
			if obj_qs.exists() and obj_qs.count() == 1:
				instance = self.model()
				instance.content = content
				instance.user = user
				instance.content_type = model_qs.first()
				instance.object_id = obj_qs.first().id
				if parent_obj:
					instance.parent = parent_obj
				instance.save()
				return instance
		return None





# Create your models here.
class Comment(models.Model):

	#attributes:
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	#relationships:
	#ForeignKey, Many to one: many comments should have One user and Many comments have One posts
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
	#post = models.ForeignKey(Post, on_delete=models.CASCADE)

	#GenericForeignKey, it's related to any model and is more dynamic, info: DjangoDocumentation
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	#intance:
	objects = CommentManager()


	class Meta:
		verbose_name = "Comment"
		verbose_name_plural = "Comments"
		ordering = ['-timestamp']

	def __str__(self):
		return self.user.username

	#get_absolute_urlf: ger url, redirect to comments:detail and pass the id to function in views
	def get_absolute_urlf(self):
		#return reverse_lazy('posts:detail', kwargs={'id': self.id}) with id, info: after doing slugify and signals
		return reverse_lazy('comments:detail', kwargs={'id': self.id})

	# get_absolute_url is the same but like property
	@property
	def get_absolute_url(self):
	#return reverse_lazy('posts:detail', kwargs={'id': self.id}) with id, info: after doing slugify and signals
		return reverse_lazy('posts:list')

	# get_delete_url: redirect to comments delete whot id form param in tamplat
	def get_delete_url(self):
		return reverse_lazy('comments:delete', kwargs={'id': self.id})
	# children: filter comments whit the parent self, its say id comment !
	def children(self):
		return Comment.objects.filter(parent=self)

	# is_parent: if have parent its true
	@property
	def is_parent(self):
		if self.parent is not None:
			return False

			






