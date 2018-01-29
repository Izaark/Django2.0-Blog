''' serializers.py convert models, and instances in Python datatypes its say in JSON 
	info: info: http://www.django-rest-framework.org/api-guide/serializers/ '''

from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin

from users.api.serializers import UserListSerializer
User = get_user_model()

''' importante: crea un comentario desde rest framewrok con un model(post), slug(ark), parent_id(solo si es comm padre)
 y user, todo viene desde el request del client y se pasan estos parametros en views, nota: se hace asi por usar ContentType
 y todo lo relacionado a llaves genericas, es mas complicado pero ayuda mucho ! '''
 # create_comment_serializer: create a comment from rest framewrok, and return class CommentCreateSeralize  !!
def create_comment_serializer(model_type=None, slug=None, parent_id=None, user=None):
	# set in url: example: http://localhost:8000/api/comments/create/?type=post&slug=ark&parent_id=67
	class CommentCreateSeralize(ModelSerializer):
		class Meta:
			model = Comment
			fields = ['id', 'content', 'timestamp']

		def __init__(self, *args, **kwargs):
			self.model_type = model_type
			self.slug = slug
			self.parent_obj = None

			# only exec if the cooment created is child
			if parent_id:
				parent_qs = Comment.objects.filter(id=parent_id)
				if parent_qs.exists() and parent_qs.count() == 1:
					self.parent_obj = parent_qs.first()
			return super(CommentCreateSeralize, self).__init__(*args, **kwargs)

		# validate: valid if the model and the object is ok, return data from endpoint
		def validate(self, data):
			model_type = self.model_type
			model_qs = ContentType.objects.filter(model=model_type)
			if not model_qs.exists() or model_qs.count() != 1:
				raise ValidationError("No es tipo de contenido valido !")
			SomeModel = model_qs.first().model_class()
			obj_qs = SomeModel.objects.filter(slug=self.slug)
			if not obj_qs.exists() or obj_qs.count() != 1:
				raise ValidationError("Esto no es un slug para el tipo de contenido")
			return data

		# create: once done validation, it's create the comment !
		def create(self, validated_data):
			content = validated_data.get('content')
			if user:
				main_user = user
			else:
				main_user = User.objects.all().first()
			model_type = self.model_type
			slug = self.slug
			parent_obj = self.parent_obj
			# create_by_model_type comes from models !
			comment = Comment.objects.create_by_model_type(
						model_type, slug, content, main_user,
						parent_obj=parent_obj,
					)
			return comment

	return CommentCreateSeralize

# CommentListSerializer: serialize cooment's List
class CommentListSerializer(ModelSerializer):
	# reply_count: serialize field for add more data !
	reply_count = SerializerMethodField()
	url = HyperlinkedIdentityField(view_name='comments-api:thread') #get the comment url !
	class Meta:
		model = Comment
		fields = ['url','id', 'content', 'timestamp', 'reply_count']

	# get_reply_count: get children function from Comment model and return count, func: it's necesary for each SerializerMethodField
	def get_reply_count(self, obj):
			return obj.children().count()


# TODO: by error: yperlinkedIdentityField` requires the request in the serializer context. Add `context={'request': request}
# CommentPostsSerializer: to posts url in fields
class CommentPostsSerializer(ModelSerializer):
	# reply_count: serialize field for add more data !
	reply_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = ['id', 'content', 'timestamp', 'reply_count']

	# get_reply_count: get children function from Comment model and return count, func: it's necesary for each SerializerMethodField
	def get_reply_count(self, obj):
			return obj.children().count()

# CommentSerializer: serialize cooment's List
class CommentSerializer(ModelSerializer):
	# reply_count: serialize field for add more data !
	reply_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = ['id', 'content', 'timestamp', 'reply_count', 'object_id']

	# get_reply_count: get children function from Comment model and return count, func: it's necesary for each SerializerMethodField
	def get_reply_count(self, obj):
			return obj.children().count()

# CommentChildSerializer: serialize data for comments children
class CommentChildSerializer(ModelSerializer):
		user = UserListSerializer(read_only=True)
		class Meta:
			model = Comment
			fields = ['id', 'content', 'timestamp', 'user']

# CommentSerializer: serialize comment's detail
class CommentDetailSerializer(ModelSerializer):
	replies = SerializerMethodField()
	reply_count = SerializerMethodField()
	content_object_url = SerializerMethodField()
	user = UserListSerializer(read_only=True)
	class Meta:
		model = Comment

		fields = ['id', 'content', 'timestamp', 'content_type', 'object_id', 'content_object_url', 'parent', 'user', 'reply_count', 'replies']
		read_only_fields = ['content_type', 'object_id', 'parent', 'user']

	# get_content_object_url: get post url from posts get_api_url
	def get_content_object_url(self, obj):
		try:
			return obj.content_object.get_api_url()
		except:
			return None

	# get_replies: return all data serialize from CommentChildSerializer with children function
	def get_replies(self, obj):
			return CommentChildSerializer(obj.children(), many=True).data

	def get_reply_count(self, obj):
			return obj.children().count()
			# fix !
			# if obj.is_parent:
			# 	return obj.children().count()
			# return 0

