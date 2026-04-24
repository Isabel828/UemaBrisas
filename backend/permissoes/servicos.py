from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound, ValidationError

from .models import PerfilAcesso


def obter_ou_criar_perfil(usuario: User) -> PerfilAcesso:
    perfil, _ = PerfilAcesso.objects.get_or_create(
        usuario=usuario,
        defaults={
            'role': 'Atendente',
            'superusuario': False,
            'admin_municipio': False,
            'profissional_interno': True,
            'usuario_externo': False,
            'visualizar': True,
            'editor': False,
            'comentar': True,
            'aprovar': False,
            'assinar': False,
            'exportar': False,
        }
    )
    return perfil


def listar_usuarios_com_perfil():
    usuarios = User.objects.all().order_by('id')
    resultado = []

    for usuario in usuarios:
        perfil = obter_ou_criar_perfil(usuario)
        resultado.append({
            'usuario': usuario,
            'perfil': perfil,
        })

    return resultado


def buscar_usuario_por_id(usuario_id: int) -> User:
    usuario = User.objects.filter(id=usuario_id).first()
    if not usuario:
        raise NotFound('Usuario nao encontrado.')
    return usuario


def buscar_perfil_por_usuario_id(usuario_id: int) -> PerfilAcesso:
    usuario = buscar_usuario_por_id(usuario_id)
    return obter_ou_criar_perfil(usuario)


def atualizar_perfil_usuario(usuario_id: int, dados: dict) -> PerfilAcesso:
    perfil = buscar_perfil_por_usuario_id(usuario_id)

    if perfil.superusuario and dados.get('usuario_externo') is True:
        raise ValidationError('Nao e permitido transformar superusuario em usuario externo.')

    for campo, valor in dados.items():
        setattr(perfil, campo, valor)

    perfil.save()
    return perfil


def montar_resposta_perfil(perfil: PerfilAcesso) -> dict:
    usuario = perfil.usuario
    nome = f'{usuario.first_name} {usuario.last_name}'.strip() or usuario.username

    return {
        'id': usuario.id,
        'name': nome,
        'email': usuario.email,
        'role': perfil.role,
        'flags': {
            'superusuario': perfil.superusuario,
            'adminMunicipio': perfil.admin_municipio,
            'profissionalInterno': perfil.profissional_interno,
            'usuarioExterno': perfil.usuario_externo,
        },
        'permissions': {
            'visualizar': perfil.visualizar,
            'editor': perfil.editor,
            'comentar': perfil.comentar,
            'aprovar': perfil.aprovar,
            'assinar': perfil.assinar,
            'exportar': perfil.exportar,
        }
    }


def listar_permissoes_disponiveis() -> dict:
    return {
        'roles': ['Admin', 'Tecnico', 'Juridico', 'Atendente', 'Gestor', 'Auditor'],
        'flags': [
            'superusuario',
            'admin_municipio',
            'profissional_interno',
            'usuario_externo',
        ],
        'acoes': [
            'visualizar',
            'editor',
            'comentar',
            'aprovar',
            'assinar',
            'exportar',
        ]
    }


# 🔥 ESSA É A PARTE QUE FALTAVA (IMPORTANTE PRO FRONTEND)
def obter_permissoes_usuario(user):
    perfil = obter_ou_criar_perfil(user)

    return {
        "roles": [perfil.role],
        "flags": [
            flag for flag, ativo in {
                "superusuario": perfil.superusuario,
                "admin_municipio": perfil.admin_municipio,
                "profissional_interno": perfil.profissional_interno,
                "usuario_externo": perfil.usuario_externo,
            }.items() if ativo
        ],
        "acoes": [
            acao for acao, ativo in {
                "visualizar": perfil.visualizar,
                "editor": perfil.editor,
                "comentar": perfil.comentar,
                "aprovar": perfil.aprovar,
                "assinar": perfil.assinar,
                "exportar": perfil.exportar,
            }.items() if ativo
        ]
    }