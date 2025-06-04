from django.contrib import admin


# Classe base para Inlines com permissão de edição apenas na triagem
class InlineRestricaoAlteracao(admin.TabularInline):  # ou StackedInline se necessário
    extra = 0

    def is_triagem_view(self, request):
        url_name = getattr(request.resolver_match, 'url_name', '')
        return url_name.startswith('triagem') or 'triagem' in request.META.get('HTTP_REFERER', '')

    def has_change_permission(self, request, obj=None):
        return self.is_triagem_view(request)

    def has_add_permission(self, request, obj=None):
        return self.is_triagem_view(request)

    def has_delete_permission(self, request, obj=None):
        return self.is_triagem_view(request)

    def get_readonly_fields(self, request, obj=None):
        if not self.is_triagem_view(request):
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)
