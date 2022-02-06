from rest_framework import permissions
from .models import Contributor, Issue, Comment


class IsOwner(permissions.BasePermission):

    def check_object_permission(self, request, view, obj):
        return request.user == obj.author_user_id


class IsOwnerOrContributorReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # If user is creator of the object, has all rights
        if obj.author_user_id == request.user:
            return True
        if isinstance(obj, Issue):
            obj = obj.project_id
        if isinstance(obj, Comment):
            obj = obj.issue_id.project_id
        # If user is assigned, he gets read_only rights
        if Contributor.objects.filter(project=obj, user=request.user).first() and (request.method in permissions.SAFE_METHODS or request.method == "POST"):
            return True
        return False
