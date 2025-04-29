from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Moders").exists():
            return True
        return False


class NotIsModer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.groups.filter(name="Moders").exists():
            return True
        return False


class IsSubscriber(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.subscriptions.filter(id=obj.id).exists():
            return True
        return False
