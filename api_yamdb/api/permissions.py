from rest_framework.permissions import SAFE_METHODS, BasePermission


class SingleBasePermission(BasePermission):
    """
    Базовый класс для разрешений с одинаковыми
    правилами доступа для отдельного объекта и для списка объектов
    """
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdmin(SingleBasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsModer(SingleBasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_moderator)


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and obj.author == request.user)


class IsRead(SingleBasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
