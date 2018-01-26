''' permission.py genereate permissions for app, 
	info: http://www.django-rest-framework.org/api-guide/permissions/ '''

from rest_framework.permissions import BasePermission

# IsOwnerOrReadOnly: check if method that user request is ok and the user have the correct permission for updating, or deleting
class IsOwnerOrReadOnly(BasePermission):
	message = 'Debes ser el propietario de esto , para realizar la consulta !!'
	my_safe_method = ['GET', 'PUT', 'DELETE']

	def has_permission(self, request, view):
		if request.method in self.my_safe_method:
			return True
		return False

	def has_object_permission(self, request, view, obj):
		return obj.user == request.user