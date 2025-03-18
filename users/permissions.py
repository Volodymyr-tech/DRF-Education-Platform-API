from rest_framework import permissions


class IsOwnerOrModer(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        #so we'll always allow GET, HEAD or OPTIONS requests.

        if request.user.groups.filter(name="Moders").exists():
            return True

        return obj.owner == request.user


# class IsModer(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an object to edit it.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         if request.user.groups.filter(name="Moders").exists():
#             return True
#         return False