from rest_framework.permissions import BasePermission


class EhAdministradorOuSuperusuario(BasePermission):
    message = 'Apenas administradores podem realizar esta acao.'

    def has_permission(self, request, view):
        usuario = request.user

        if not usuario or not usuario.is_authenticated:
            return False

        if usuario.is_superuser:
            return True

        perfil = getattr(usuario, 'perfil_acesso', None)
        if not perfil:
            return False

        return perfil.superusuario or perfil.admin_municipio


class PodeVisualizarProprioPerfilOuSerAdmin(BasePermission):
    message = 'Voce nao tem permissao para acessar este recurso.'

    def has_permission(self, request, view):
        usuario = request.user
        if not usuario or not usuario.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        usuario = request.user

        if usuario.is_superuser:
            return True

        perfil = getattr(usuario, 'perfil_acesso', None)
        if perfil and (perfil.superusuario or perfil.admin_municipio):
            return True

        return obj.usuario_id == usuario.id
