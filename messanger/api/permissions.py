from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method not in ("GET", "OPTIONS"):
            if request.user.is_authenticated:
                if request.user == obj.host:
                    return True
            return False
        return True
    

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in ("GET", "OPTIONS"):
            if request.user.is_superuser:
                if obj.is_superuser:
                    return False
                return True
            elif request.user == obj:
                return True
            else:
                return False
        return True


class IsEditorPermission(permissions.DjangoModelPermissions):

    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
