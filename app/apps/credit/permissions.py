from rest_framework import permissions


class BranchCloseAccountPermission(permissions.BasePermission):
    message = 'The account opening branch can close the account'

    def has_object_permission(self, request, view, obj):
        if view.action in ('update', 'partial_update'):
            return request.user.pk == obj.branch.pk
        return True
