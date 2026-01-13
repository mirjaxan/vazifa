from rest_framework.permissions import BasePermission 

from api.models import DONE

class IsAuthiticantedAndAuthor(BasePermission): 
	def has_permission(self, request, view):
			return request.user.is_authenticated
	
	def has_object_permission(self, request, view, obj):
			return obj.user == request.user


class isAuthenticatedAndDone(BasePermission):
	def has_permission(self, request, view):
			return request.user.is_authenticated and request.user.status  == DONE 