# api_mobile_views.py
"""
API para aplicativo mobile de cadastro de CRR.
Autenticação via API Key (header X-API-Key).
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import DispositivoMobile, TabelaEnquadramento, Agente
from .permissions import IsDispositivoMobile
from .serializers import (
    DispositivoSerializer,
    CrrMobileSerializer,
    TabelaEnquadramentoSerializer,
)


# ==================== ATIVACAO E LOGIN ==================== #

@api_view(['POST'])
@permission_classes([AllowAny])
def ativar_dispositivo(request):
    """
    Ativa um dispositivo mobile usando o codigo de ativacao.

    POST /api/v1/mobile/ativar/
    {
        "codigo": "123456",
        "matricula": "12345"
    }

    Retorna a API Key para autenticacao nas proximas requests.
    """
    codigo = request.data.get('codigo', '').strip()
    matricula = request.data.get('matricula', '').strip()

    if not codigo:
        return Response({
            'sucesso': False,
            'erro': 'Codigo de ativacao e obrigatorio'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        dispositivo = DispositivoMobile.objects.get(codigo_ativacao=codigo)
    except DispositivoMobile.DoesNotExist:
        return Response({
            'sucesso': False,
            'erro': 'Codigo de ativacao invalido'
        }, status=status.HTTP_404_NOT_FOUND)

    if not dispositivo.ativo:
        return Response({
            'sucesso': False,
            'erro': 'Dispositivo desativado. Contate o administrador.'
        }, status=status.HTTP_403_FORBIDDEN)

    # Valida matricula do agente
    if not matricula:
        return Response({
            'sucesso': False,
            'erro': 'Matricula do agente e obrigatoria'
        }, status=status.HTTP_400_BAD_REQUEST)

    senha = request.data.get('senha', '').strip()
    if not senha:
        return Response({
            'sucesso': False,
            'erro': 'Senha e obrigatoria'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        agente = Agente.objects.get(matricula=matricula)
        if not agente.ativo:
            return Response({
                'sucesso': False,
                'erro': 'Agente desativado. Contate o administrador.'
            }, status=status.HTTP_403_FORBIDDEN)
    except Agente.DoesNotExist:
        return Response({
            'sucesso': False,
            'erro': 'Matricula nao cadastrada. Contate o administrador.'
        }, status=status.HTTP_404_NOT_FOUND)

    # Valida senha do agente
    if not agente.check_senha(senha):
        return Response({
            'sucesso': False,
            'erro': 'Senha incorreta'
        }, status=status.HTTP_403_FORBIDDEN)

    from django.utils import timezone
    dispositivo.ativado = True
    dispositivo.ultimo_acesso = timezone.now()
    dispositivo.save()

    return Response({
        'sucesso': True,
        'mensagem': 'Dispositivo ativado com sucesso',
        'dispositivo': DispositivoSerializer(dispositivo).data,
        'senha_alterada': agente.senha_alterada,
        'assinatura_url': request.build_absolute_uri(agente.assinatura.url) if agente.assinatura else None,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_dispositivo(request):
    """
    Registra um novo dispositivo mobile via IMEI.

    POST /api/v1/mobile/registrar/
    {
        "nome": "Tablet Agente 01",
        "imei": "123456789012345",
        "matricula": "12345"
    }

    Se o dispositivo ja existir (mesmo IMEI), retorna os dados do dispositivo existente.
    O dispositivo deve ser ativado pelo administrador no painel web.
    """
    imei = request.data.get('imei')
    nome = request.data.get('nome', 'Dispositivo Mobile')
    matricula = request.data.get('matricula', '')

    # Verifica se dispositivo ja existe com este IMEI
    dispositivo = DispositivoMobile.objects.filter(imei=imei).first()

    if dispositivo:
        # Atualiza ultimo acesso
        from django.utils import timezone
        dispositivo.ultimo_acesso = timezone.now()
        dispositivo.save()

        return Response({
            'sucesso': True,
            'mensagem': 'Dispositivo encontrado',
            'dispositivo': DispositivoSerializer(dispositivo).data,
            'novo': False
        })

    # Cria novo dispositivo
    dispositivo = DispositivoMobile.objects.create(
        nome=nome,
        imei=imei,
    )

    return Response({
        'sucesso': True,
        'mensagem': 'Dispositivo registrado. Aguarde a ativacao pelo administrador.',
        'dispositivo': DispositivoSerializer(dispositivo).data,
        'novo': True
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_dispositivo(request):
    """
    Login de dispositivo existente via IMEI.

    POST /api/v1/mobile/login/
    {
        "imei": "123456789012345"
    }

    Retorna dados do dispositivo.
    """
    imei = request.data.get('imei')

    if not imei:
        return Response({
            'sucesso': False,
            'erro': 'IMEI e obrigatorio'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        dispositivo = DispositivoMobile.objects.get(imei=imei)

        if not dispositivo.ativo:
            return Response({
                'sucesso': False,
                'erro': 'Dispositivo desativado. Contate o administrador.'
            }, status=status.HTTP_403_FORBIDDEN)

        # Atualiza ultimo acesso
        from django.utils import timezone
        dispositivo.ultimo_acesso = timezone.now()
        dispositivo.save()

        return Response({
            'sucesso': True,
            'dispositivo': DispositivoSerializer(dispositivo).data,
        })

    except DispositivoMobile.DoesNotExist:
        return Response({
            'sucesso': False,
            'erro': 'Dispositivo nao registrado. Faca o registro primeiro.'
        }, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsDispositivoMobile])
def obter_proximo_numero(request):
    """
    Retorna o proximo numero CRR disponivel.
    Gera sequencialmente a partir do maior numeroCrr existente.

    GET /api/v1/mobile/crr/proximo-numero/
    Header: X-API-Key: <api_key>
    """
    from .models import Crr
    from django.db.models import Max, IntegerField
    from django.db.models.functions import Cast, Substr

    resultado = Crr.objects.filter(
        numeroCrr__regex=r'^[eE]\d+'
    ).annotate(
        num_part=Cast(Substr('numeroCrr', 2), IntegerField())
    ).aggregate(max_num=Max('num_part'))

    proximo = (resultado['max_num'] or 0) + 1
    numero_formatado = f"E{proximo:04d}"

    return Response({
        'sucesso': True,
        'proximo_numero': numero_formatado,
    })


# ==================== CRUD DE CRR ==================== #

@api_view(['GET'])
@permission_classes([IsDispositivoMobile])
def listar_crrs(request):
    """
    Lista os CRRs criados pelo agente do dispositivo.

    GET /api/v1/mobile/crr/
    Header: X-API-Key: <api_key>
    """
    from .models import Crr
    from .serializers import CrrMobileReadSerializer
    matricula = request.headers.get('X-Matricula', '').strip()

    crrs = Crr.objects.filter(
        matriculaAgente=matricula
    ).prefetch_related(
        'veiculo', 'condutores', 'aits',
        'enquadramentos__enquadramento',
    ).order_by('-criado_em')[:10]

    return Response({
        'sucesso': True,
        'total': crrs.count(),
        'crrs': CrrMobileReadSerializer(crrs, many=True).data
    })


@api_view(['GET'])
@permission_classes([IsDispositivoMobile])
def buscar_crrs(request):
    """
    Busca CRRs por filtros: placa, marca, modelo, data.

    GET /api/v1/mobile/crr/buscar/?placa=ABC&marca=FORD&modelo=FIESTA&data=2024-01-01
    Header: X-API-Key: <api_key>
    """
    from .models import Crr
    from .serializers import CrrMobileReadSerializer

    placa = request.query_params.get('placa', '').strip()
    marca = request.query_params.get('marca', '').strip()
    modelo = request.query_params.get('modelo', '').strip()
    data = request.query_params.get('data', '').strip()

    if not any([placa, marca, modelo, data]):
        return Response({
            'sucesso': False,
            'erro': 'Informe ao menos um filtro de busca'
        }, status=status.HTTP_400_BAD_REQUEST)

    crrs = Crr.objects.prefetch_related(
        'veiculo', 'condutores', 'aits',
        'enquadramentos__enquadramento',
    )

    if placa:
        crrs = crrs.filter(veiculo__placa__icontains=placa)
    if marca:
        crrs = crrs.filter(veiculo__marca__icontains=marca)
    if modelo:
        crrs = crrs.filter(veiculo__modelo__icontains=modelo)
    if data:
        crrs = crrs.filter(dataFiscalizacao=data)

    crrs = crrs.order_by('-criado_em')[:20]

    return Response({
        'sucesso': True,
        'total': crrs.count(),
        'crrs': CrrMobileReadSerializer(crrs, many=True).data
    })


@api_view(['POST'])
@permission_classes([IsDispositivoMobile])
def criar_crr(request):
    """
    Cria um novo CRR.

    POST /api/v1/mobile/crr/
    Header: X-API-Key: <api_key>

    O numeroCrr deve ser do lote atribuído ao dispositivo.
    """
    serializer = CrrMobileSerializer(data=request.data)

    if serializer.is_valid():
        crr = serializer.save()
        return Response({
            'sucesso': True,
            'mensagem': f'CRR {crr.numeroCrr} criado com sucesso',
            'crr': CrrMobileSerializer(crr).data
        }, status=status.HTTP_201_CREATED)

    return Response({
        'sucesso': False,
        'erros': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
@permission_classes([IsDispositivoMobile])
def atualizar_condutor_crr(request, crr_id):
    """
    Atualiza situacaoEntrega e/ou assinaturaCondutor de um CRR existente.

    PATCH /api/v1/mobile/crr/<crr_id>/atualizar-condutor/
    Header: X-API-Key: <api_key>
    {
        "situacaoEntrega": "Assinou e recebeu 2a via",
        "assinaturaCondutor": "<base64_png>"
    }

    Apenas o agente que criou o CRR pode atualiza-lo.
    """
    from .models import Crr

    matricula = request.headers.get('X-Matricula', '').strip()

    try:
        crr = Crr.objects.get(id=crr_id, matriculaAgente=matricula)
    except Crr.DoesNotExist:
        return Response(
            {'sucesso': False, 'erro': 'CRR nao encontrado'},
            status=status.HTTP_404_NOT_FOUND,
        )

    SITUACOES_VALIDAS = {
        'Condutor ausente',
        'Assinou e recebeu 2a via',
        'Recusou assinar e recebeu 2a via',
        'Recusou assinar e a receber 2a via',
    }

    situacao = request.data.get('situacaoEntrega', '').strip()
    assinatura = request.data.get('assinaturaCondutor', '')

    if situacao and situacao not in SITUACOES_VALIDAS:
        return Response(
            {'sucesso': False, 'erro': 'Situacao de entrega invalida'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if situacao:
        crr.situacaoEntrega = situacao
        crr.save(update_fields=['situacaoEntrega'])

    if assinatura is not None:
        condutor = crr.condutores.first()
        if condutor:
            condutor.assinaturaCondutor = assinatura
            condutor.save(update_fields=['assinaturaCondutor'])

    return Response({'sucesso': True, 'mensagem': 'Condutor atualizado com sucesso'})


# ==================== DADOS AUXILIARES ==================== #

@api_view(['GET'])
@permission_classes([IsDispositivoMobile])
def listar_enquadramentos(request):
    """
    Lista todos os enquadramentos disponíveis.

    GET /api/v1/mobile/enquadramentos/
    Header: X-API-Key: <api_key>
    """
    enquadramentos = TabelaEnquadramento.objects.all().order_by('codigo')
    serializer = TabelaEnquadramentoSerializer(enquadramentos, many=True)

    return Response({
        'sucesso': True,
        'total': enquadramentos.count(),
        'enquadramentos': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsDispositivoMobile])
def status_dispositivo(request):
    """
    Retorna status completo do dispositivo.

    GET /api/v1/mobile/status/
    Header: X-API-Key: <api_key>
    """
    dispositivo = request.dispositivo

    return Response({
        'sucesso': True,
        'dispositivo': {
            'id': dispositivo.id,
            'nome': dispositivo.nome,
            'imei': dispositivo.imei,
            'ativo': dispositivo.ativo,
            'ultimo_acesso': dispositivo.ultimo_acesso,
        },
    })


# ==================== VALIDAÇÃO DE LOGIN ==================== #

@api_view(['POST'])
@permission_classes([AllowAny])
def validar_login(request):
    """
    Valida login do app mobile: verifica api_key + matricula.
    Garante que o agente existe, esta ativo e corresponde ao dispositivo.

    POST /api/v1/mobile/validar-login/
    {
        "api_key": "abc123...",
        "matricula": "12345"
    }
    """
    api_key = request.data.get('api_key', '').strip()
    matricula = request.data.get('matricula', '').strip()
    senha = request.data.get('senha', '').strip()

    if not api_key or not matricula or not senha:
        return Response({
            'sucesso': False,
            'erro': 'API Key, matricula e senha sao obrigatorios'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Valida dispositivo
    try:
        dispositivo = DispositivoMobile.objects.get(
            api_key=api_key, ativo=True, ativado=True
        )
    except DispositivoMobile.DoesNotExist:
        return Response({
            'sucesso': False,
            'erro': 'Dispositivo nao encontrado ou desativado'
        }, status=status.HTTP_403_FORBIDDEN)

    # Valida que o agente esta ativo
    try:
        agente = Agente.objects.get(matricula=matricula, ativo=True)
    except Agente.DoesNotExist:
        return Response({
            'sucesso': False,
            'erro': 'Agente nao cadastrado ou desativado'
        }, status=status.HTTP_403_FORBIDDEN)

    # Valida senha do agente
    if not agente.check_senha(senha):
        return Response({
            'sucesso': False,
            'erro': 'Senha incorreta'
        }, status=status.HTTP_403_FORBIDDEN)

    # Atualiza ultimo acesso
    from django.utils import timezone
    dispositivo.ultimo_acesso = timezone.now()
    dispositivo.save(update_fields=['ultimo_acesso'])

    assinatura_url = (
        request.build_absolute_uri(agente.assinatura.url)
        if agente.assinatura else None
    )
    return Response({
        'sucesso': True,
        'agente': {
            'nome': agente.nome,
            'matricula': agente.matricula,
            'assinatura_url': assinatura_url,
        },
        'senha_alterada': agente.senha_alterada,
    })


# ==================== ALTERAÇÃO DE SENHA ==================== #

@api_view(['POST'])
@permission_classes([IsDispositivoMobile])
def alterar_senha(request):
    """
    Altera a senha do agente.

    POST /api/v1/mobile/alterar-senha/
    Header: X-API-Key: <api_key>
    { "matricula": "12345", "nova_senha": "novasenha" }
    """
    matricula = request.data.get('matricula', '').strip()
    nova_senha = request.data.get('nova_senha', '').strip()

    if not matricula or not nova_senha:
        return Response({
            'sucesso': False,
            'erro': 'Matricula e nova senha sao obrigatorios'
        }, status=status.HTTP_400_BAD_REQUEST)

    if len(nova_senha) < 4:
        return Response({
            'sucesso': False,
            'erro': 'Senha deve ter no minimo 4 caracteres'
        }, status=status.HTTP_400_BAD_REQUEST)

    if nova_senha == 'admin':
        return Response({
            'sucesso': False,
            'erro': 'A nova senha nao pode ser "admin"'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        agente = Agente.objects.get(
            matricula=matricula, ativo=True
        )
        agente.set_senha(nova_senha)
        agente.senha_alterada = True
        agente.save(update_fields=['senha', 'senha_alterada'])
        return Response({
            'sucesso': True,
            'mensagem': 'Senha alterada com sucesso'
        })
    except Agente.DoesNotExist:
        return Response({
            'sucesso': False,
            'erro': 'Agente nao encontrado'
        }, status=status.HTTP_404_NOT_FOUND)


# ==================== VERSÃO DO APP ==================== #

@api_view(['GET'])
@permission_classes([AllowAny])
def app_version(request):
    """
    Retorna informações da versão atual do app.
    Usado para verificar atualizações.

    GET /api/v1/mobile/app-version/
    """
    return Response({
        'versao': '1.0.0',
        'build': 1,
        'obrigatoria': False,
        'mensagem': 'Nova versão disponível!',
        'download_url': 'http://192.168.1.71:8000/static/app/divprom-mobile.apk',
        'novidades': [
            'Correções de bugs',
            'Melhorias de performance',
        ]
    })
