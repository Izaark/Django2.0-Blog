''' serializers.py convert models, and instances in Python datatypes its say in JSON 
	info: info: http://www.django-rest-framework.org/api-guide/serializers/ '''

from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, ValidationError, EmailField,CharField
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework_jwt.settings import api_settings

User = get_user_model()
# UserListSerializer: get all user's fields
class UserListSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'email']

# UserDetailSerializer: get user's detail
class UserDetailSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'first_name', 'last_name']

# UserRegisterSerializer: register a new user with get_user_model
class UserRegisterSerializer(ModelSerializer):
	# register more fileds out modelForm
	email2 = EmailField(label='Confirmar Email')
	token = CharField(allow_blank=True, read_only=True)

	class Meta:
		model = User
		fields = ['token','username', 'email', 'email2', 'password']
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
		email1 = data.get('email2')
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

		# create token from class
		token = GenerateToken()
		validated_data['token'] = token.create(user_obj)

		return validated_data

# UserLiginSerializer: set fields for login user 
class UserLiginSerializer(ModelSerializer):
	token = CharField(allow_blank=True, read_only=True)
	username = CharField()
	email = EmailField(label='Direccion de Email')


	class Meta:
		model = User
		fields = ['token','username', 'email', 'password']
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

		# create token from class
		class_token = GenerateToken()
		#data['token'] = self.create_token(user_obj)
		data['token'] = class_token.create(user_obj)
		return data


# GenerateToken: Creating a new token manually info: http://getblimp.github.io/django-rest-framework-jwt/#additional-settings
class GenerateToken:

	def create(self, obj):
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

		payload = jwt_payload_handler(obj)
		token = jwt_encode_handler(payload)
		print('en clases')
		return token





