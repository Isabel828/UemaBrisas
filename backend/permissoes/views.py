from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissoes import EhAdministradorOuSuperusuario
from .serializadores import (
    PerfilAcessoSerializador,
    AtualizarPerfilAcessoSerializador,
)
from .servicos import (
    obter_ou_criar_perfil,
    listar_usuarios_com_perfil,
    buscar_perfil_por_usuario_id,
    atualizar_perfil_usuario,
    montar_resposta_perfil,
    listar_permissoes_disponiveis,
    obter_permissoes_usuario,  # 🔥 IMPORTANTE
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def minhas_permissoes(request):
    perfil = obter_ou_criar_perfil(request.user)
    return Response(montar_resposta_perfil(perfil))


# 🔥 NOVA VIEW PRA FRONTEND
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def minhas_regras(request):
    return Response(obter_permissoes_usuario(request.user))


@api_view(['GET'])
@permission_classes([IsAuthenticated, EhAdministradorOuSuperusuario])
def listar_usuarios_permissoes(request):
    registros = listar_usuarios_com_perfil()
    resposta = []

    for item in registros:
        resposta.append(montar_resposta_perfil(item['perfil']))

    return Response(resposta)


@api_view(['GET'])
@permission_classes([IsAuthenticated, EhAdministradorOuSuperusuario])
def detalhar_permissoes_usuario(request, usuario_id):
    perfil = buscar_perfil_por_usuario_id(usuario_id)
    serializador = PerfilAcessoSerializador(perfil)
    return Response(serializador.data)


@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated, EhAdministradorOuSuperusuario])
def atualizar_permissoes_usuario(request, usuario_id):
    perfil = buscar_perfil_por_usuario_id(usuario_id)
    parcial = request.method == 'PATCH'

    serializador = AtualizarPerfilAcessoSerializador(
        perfil,
        data=request.data,
        partial=parcial
    )
    serializador.is_valid(raise_exception=True)

    perfil_atualizado = atualizar_perfil_usuario(
        usuario_id,
        serializador.validated_data
    )
    resposta = PerfilAcessoSerializador(perfil_atualizado)
    return Response(resposta.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, EhAdministradorOuSuperusuario])
def listar_regras_disponiveis(request):
    return Response(listar_permissoes_disponiveis())