''' serializers.py convert models, and instances in Python datatypes its say in JSON 
	info: info: http://www.django-rest-framework.org/api-guide/serializers/ '''

from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, ValidationError, EmailField,CharField
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


# UserListSerializer: get all user's fields
class UserListSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'email']

# UserDetailSerializer: get some fields to posts and comments user field!
class UserDetailSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'first_name', 'last_name']

# UserRegisterSerializer: register a new user with get_user_model
class UserRegisterSerializer(ModelSerializer):
	# register more fileds out modelForm
	email2 = EmailField(label='Confirmar Email')
	class Meta:
		model = User
		fields = ['username', 'email', 'email2', 'password']
		extra_kwargs = {'password': { 'write_only': True}}

	#validate_email: valid if email1 its equals to emal2, and if email exists in db
	def validate_email(self, value):
		data = self.get_initial()
		email1 = data.get('email2')
		email2 = value
		if email1 != email2:
			raise ValidationError("Los email no coinciden")
		user_qs = User.objects.filter(email=email2)
		if user_qs.exists():
			raise ValidationError('Este usuario ya esta registrado')
		return value

	# validate_email2: valid if email2 its equals to emal1
	def validate_email2(self, value):
		data = self.get_initial()
		email1 = data.get('email1')
		email2 = value
		if email1 != email2:
			raise ValidationError("Los email no coinciden")
		return value

	# create: if validatedits ok, get data and save a new user
	def create(self, validated_data):
		username = validated_data['username']
		email = validated_data['email']
		password = validated_data['password']
		user_obj = User(username=username, email=email)
		user_obj.set_password(password)
		user_obj.save()
		return validated_data


# UserLiginSerializer: set fields for login user 
class UserLiginSerializer(ModelSerializer):
	token = CharField(allow_blank=True, read_only=True)
	username = CharField()
	email = EmailField(label='Direccion de Email')
	class Meta:
		model = User
		fields = ['token','username', 'email']
		extra_kwargs = {'password': { 'write_only': True}}


	# validate: valid if email, username, password are correct !
	def validate(self, data):
		user_obj = None
		email = data.get('email', None)
		username = data.get('username', None)
		password = data['password']
		if not email and not username:
			raise ValidationError('El username o email is requerido para entrar')

		# filter user by email, password, compare if are equals, and exclude others emails
		user = User.objects.filter(Q(email=email) | Q(username=username)).distinct()
		user = user.exclude(email__isnull=True).exclude(email__iexact='')
		if user.exists() and user.count() == 1:
			user_obj = user.first()
		else:
			raise ValidationError('Este username / email no es valido')

		if user_obj:
			if not user_obj.check_password(password):
				raise ValidationError('Las credencilas son incorrectas, intenta otra vez')

		data['token'] = 'random token'
		return data



