
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CrrViewSet,VeiculoViewSet,CondutorViewSet, AitViewSet,
                    TabelaEnquadramentoViewSet, EnquadramentoViewSet)

router = DefaultRouter()
router.register(r'crr', CrrViewSet)
router.register(r'veiculo', VeiculoViewSet)
router.register(r'condutores', CondutorViewSet)
router.register(r'aits', AitViewSet)
router.register(r'tabelaenquadramento', TabelaEnquadramentoViewSet)
router.register(r'enquadramento', EnquadramentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]