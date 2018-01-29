''' pagination.py provides a few classes that help you manage paginated data – that is, 
data that’s split across several pages, with “Previous/Next” link info: http://www.django-rest-framework.org/api-guide/pagination/'''
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response



# PostLimitOffSetPagination: Looking up multiple database records, with default records, and a limit for the client !
class PostLimitOffSetPagination(LimitOffsetPagination):
	default_limit = 2
	max_limit = 2

# PostPageNumberPagination: This pagination style accepts a single number page in the request query parameters.
class PostPageNumberPagination(PageNumberPagination):
	page_size = 10

#CustomPagination: replace the default pagination output style with a modified format !
class CustomPagination(PageNumberPagination):
	page_size = 20
	def get_paginated_response(self, data):
		return Response({
			'links': {
				'next': self.get_next_link(),
				'previous': self.get_previous_link()			
			},
			'count': self.page.paginator.count,
			'response': data,
			'code':  200
			})