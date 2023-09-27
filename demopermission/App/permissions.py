from rest_framework import permissions


class HasPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        required_privilege = getattr(view, "required_privilege", [])
        user_privileges = list(user.role.role_permissions.values_list('name', flat=True))

        if not all(map(lambda v: v in user_privileges, required_privilege)):
            return False

        return True