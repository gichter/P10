from rest_framework import permissions
from .models import Contributor, Issue, Comment


class IsOwner(permissions.BasePermission):

    def check_object_permission(self, request, view, obj):
        return request.user == obj.author_user_id


class IsOwnerOrContributorReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if isinstance(obj, Issue):
            obj = obj.project_id
        if isinstance(obj, Comment):
            obj = obj.issue_id.project_id
        if obj.author_user_id == request.user:
            return True
        elif Contributor.objects.filter(project=obj, user=request.user).first() and request.method in permissions.SAFE_METHODS:
            return True
        return False
