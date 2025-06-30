from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsJavaUser(BasePermission):
    """
    Permite apenas ao usuário 'java' fazer GET e POST.
    Bloqueia PUT, PATCH, DELETE.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Permite apenas ao usuário 'java'
        if user.username != 'java':
            return False

        # Permite apenas GET (list/detail) e POST (create)
        if request.method in SAFE_METHODS or request.method == 'POST':
            return True

        return False
