''' serializers.py convert models, and instances in Python datatypes its say in JSON 
	info: info: http://www.django-rest-framework.org/api-guide/serializers/ '''

from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from comments.models import Comment


# CommentListSerializer: serialize cooment's List
class CommentListSerializer(ModelSerializer):
	# reply_count: serialize field for add more data !
	reply_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = ['id', 'content', 'timestamp', 'object_id', 'reply_count']

	# get_reply_count: get children function from Comment model and return count, func: it's necesary for each SerializerMethodField
	def get_reply_count(self, obj):
			return obj.children().count()

# CommentChildSerializer: serialize data for comments children
class CommentChildSerializer(ModelSerializer):
		class Meta:
			model = Comment
			fields = ['id', 'user', 'content', 'timestamp']

# CommentSerializer: serialize comment's detail
class CommentDetailSerializer(ModelSerializer):
	replies = SerializerMethodField()
	reply_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = ['id', 'user', 'content', 'timestamp', 'content_type', 'object_id','parent', 'reply_count', 'replies']

	# get_replies: return all data serialize from CommentChildSerializer with children function
	def get_replies(self, obj):
			return CommentChildSerializer(obj.children(), many=True).data

	def get_reply_count(self, obj):
			return obj.children().count()

