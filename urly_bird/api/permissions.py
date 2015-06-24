from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user == obj.user

class OwnsRelatedBookmark(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.bookmark.user


class IsAnonymous(permissions.BasePermission):
    def has_permission(self, request, view, obj):
        try:
            return request.user is not None
        except:
            return False