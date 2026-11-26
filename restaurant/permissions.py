from rest_framework import permissions

def is_manager(user):
    return user.groups.filter(name='managers').exists()

def is_waiter(user):
    return user.groups.filter(name='waiters').exists()

class IsManagerOrWaiterReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return is_waiter(request.user) or is_manager(request.user)
        return is_manager(request.user)


class IsManagerOrWaiterNoDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return is_manager(request.user)
        return is_manager(request.user) or is_waiter(request.user)

class IsManagerOrWaiter(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_waiter(request.user) or is_manager(request.user)