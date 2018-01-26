''' serializers.py convert models, and instances in Python datatypes its say in JSON 
	info: info: http://www.django-rest-framework.org/api-guide/serializers/ '''

from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from posts.models import Post

from comments.api.serializers import CommentListSerializer
from comments.models import Comment


# PostlistSerializer: serialize post's List
class PostListSerializer(ModelSerializer):
	#TODO: fix it, HyperlinkedIdentityField it doesn't work
	# url_list= HyperlinkedIdentityField(view_name='posts-api:detail', lookup_field='slug')

	user = SerializerMethodField()
	class Meta:
		model = Post
		fields = ['id', 'user', 'title', 'slug']

	def get_user(self, obj):
		return obj.user.username
# PostDetailSerializer: serialize each post's data
class PostDetailSerializer(ModelSerializer):

	# SerializerMethodField: It can be used to add any sort of data to the serialized representation of your object
	user = SerializerMethodField()
	image = SerializerMethodField()
	markdown = SerializerMethodField()
	comments = SerializerMethodField()

	class Meta:
		model = Post
		fields = ('id', 'user', 'title', 'slug', 'image', 'content', 'updated', 'timestamp', 'publish','read_time', 'markdown', 'comments')

	def get_user(self, obj):
		return obj.user.username

	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None		
		return image

	def get_markdown(self, obj):
		return obj.get_markdown()

	def get_comments(self, obj):
		content_type = obj.get_content_type
		objct_id = obj.id
		c_qs = Comment.objects.filter_by_instance(obj)
		comments = CommentListSerializer(c_qs, many=True).data
		return comments
# PostCreateUpdateSerializer: only serialize some fields  for updating
class PostCreateUpdateSerializer(ModelSerializer):

	class Meta:
		model = Post
		fields = ('title', 'content', 'publish', 'image')