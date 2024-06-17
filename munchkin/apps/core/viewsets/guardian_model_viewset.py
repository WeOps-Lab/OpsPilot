from django.core.exceptions import PermissionDenied
from guardian.shortcuts import assign_perm, get_objects_for_user
from rest_framework import viewsets


class GuardianModelViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet that uses django-guardian for object level permissions.
    Subclasses must define 'permission_classes' and 'guardian_serializer_class'.
    """

    # weather only superuser can access model api
    superuser_only = False

    def has_permission(self, user, obj, permission):
        """
        Check if the user has the given permission for the object.
        """
        is_auth_and_superuser = user.is_authenticated and user.is_superuser
        if self.superuser_only and not is_auth_and_superuser:
            return False

        if is_auth_and_superuser:
            return True
        elif hasattr(obj, "owner") and obj.owner == user:
            return True
        else:
            return user.has_perm(permission, obj)

    def get_queryset(self):
        """
        Override get_queryset to only include objects that the current user has
        view permission for or the current user is the owner of the object.
        """
        queryset = super().get_queryset()
        is_auth_and_superuser = self.request.user.is_authenticated and self.request.user.is_superuser
        if self.superuser_only and not is_auth_and_superuser:
            raise PermissionDenied()

        if is_auth_and_superuser:
            return queryset
        elif hasattr(queryset.model, "owner"):
            queryset = queryset.filter(owner=self.request.user)
        else:
            queryset = get_objects_for_user(self.request.user, "view", queryset)
        return queryset

    def perform_create(self, serializer):
        """
        Override perform_create to assign the created object to the current user.
        """
        obj = serializer.save()
        if hasattr(obj, "owner"):
            obj.owner = self.request.user
            obj.save()
        else:
            assign_perm("view", self.request.user, obj)
            assign_perm("change", self.request.user, obj)
            assign_perm("delete", self.request.user, obj)

    def perform_update(self, serializer):
        """
        Override perform_update to check if the current user has change permission
        for the object or the current user is the owner of the object.
        """
        if self.has_permission(self.request.user, serializer.instance, "change"):
            serializer.save()
        else:
            raise PermissionDenied()

    def perform_destroy(self, instance):
        """
        Override perform_destroy to check if the current user has delete permission
        for the object or the current user is the owner of the object.
        """
        if self.has_permission(self.request.user, instance, "delete"):
            instance.delete()
        else:
            raise PermissionDenied()
