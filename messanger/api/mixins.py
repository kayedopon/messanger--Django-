from rest_framework import permissions
from .permissions import IsOwner, IsEditorPermission, IsAccountOwner


class IsAuthenticatedEditorMixin:
    if IsEditorPermission:
        permission_classes = [permissions.IsAuthenticated, IsEditorPermission]
    else:
        permission_classes = [permissions.IsAuthenticated, IsOwner]


class IsAccountOwnerMixin:
    permission_classes  = [permissions.IsAuthenticated, IsAccountOwner]



        
