from django.db import models
from django.urls import reverse_lazy
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from .utils import get_read_time



#upload_location add dir name with id and donwn name's picture
def upload_location(instance, filename):
	return '%s/%s' %(instance.id, filename)

#PostManager override functions into models whit objects
class PostManager(models.Manager):
	#Post.object.all()
	#active: create a new function for Post model, only apears posts with filters below !!
	def active(self, *args, **kwargs):
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())
		
#Post class is the table in DB whit attributes and methods
class Post(models.Model):

	#attributes
	title = models.CharField(max_length=100)
	content = models.TextField()
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to=upload_location, null=True, blank=True, height_field='height_field', width_field='width_field')
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	read_time = models.IntegerField(default=0)

	#Relationships
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

	#instance
	objects = PostManager()


	#Meta Class: Do things apart of data up this
	class Meta:
		verbose_name = "Post"
		verbose_name_plural = "Posts"
		ordering = ['-timestamp', '-updated']#order the posts since most new to oldest

	def __str__(self):
		return self.title

	#get_absolute_urlf: ger url, redirect to posts:detail and pass the id to function in views
	def get_absolute_urlf(self):
		#return reverse_lazy('posts:detail', kwargs={'id': self.id}) with id, info: after doing slugify and signals
		return reverse_lazy('posts:detail', kwargs={'slug': self.slug})

	#get_markdown: do contetn type html in markdwon and save like safe !!!
	def get_markdown(self):
		content = self.content
		markdown_text = markdown(content)
		return mark_safe(markdown_text)

	#comments it`s a property Post. it comes from app 'commments' models.Comment.objects.filter_by_instance
	@property
	def comments(self):
		instance = self
		#qs its de function that was created as modelManager, the instance is self its say all avobe = this Post model :D
		qs = Comment.objects.filter_by_instance(instance)
		return qs

	# get_content_type: it`s a property Post. get the model fron contenttyp in db, is self its say all avobe = this Post model :D
	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type

#create_slug use for create slug whit the title name
def create_slug(instance, new_slug=None):
	slug = slugify(instance.title) #get title and slug is equals to title, generate slug with slugify module
	if new_slug is not None:	#if new_slug isn't null, slug equals to new slug
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by('-id')#queryset for filter by slug, ordering from highest to lowest
	exists = qs.exists()
	if exists:	#if exists
		new_slug = '%s-%s' %(slug, qs.first().id)	#the new_slug is equlas name slug field + firts id, example :testd22-2
		return create_slug(instance, new_slug=new_slug)	#reuturn recursive function with the new slug
	return slug	#if new_slug is Null, and queryset don't exist only reuturn slug

''' *** Las señales se usan para hacer cosas antes de guardar el objeto, esto pasa automatic., en este caso se genera una señal (translate to english)
Django provides a set of built-in signals that let user code get notified by Django itself of certain actions *** '''

#pre_save_post_receiver if haven't slug the instance.slug (instance.slug = Post.slug), create_slug do it
def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

	#assigment to instance time for reading
	if instance.content:
		html_string = instance.get_markdown()
		read_time_var = get_read_time(html_string)
		instance.read_time = read_time_var

#conntect: register the signal with the sender(remitente) Post:
pre_save.connect(pre_save_post_receiver, sender=Post)



		




