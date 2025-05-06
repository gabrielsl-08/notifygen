from rest_framework import permissions

class IsOwnerOfCrr(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        usuario = request.user  # Use `request.user` em vez de `request.usuario`
        return obj.agente_autuador == usuario  # Verifique o campo correto no modelo que associa o criador
        

            
        
