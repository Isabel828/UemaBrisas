from django.test import TestCase

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import PerfilAcesso


class PermissoesAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@email.com',
            password='12345678'
        )
        self.usuario_comum = User.objects.create_user(
            username='comum',
            email='comum@email.com',
            password='12345678'
        )

        PerfilAcesso.objects.create(
            usuario=self.admin,
            role='Admin',
            superusuario=False,
            admin_municipio=True,
            profissional_interno=True,
            usuario_externo=False,
            visualizar=True,
            editor=True,
            comentar=True,
            aprovar=True,
            assinar=True,
            exportar=True,
        )

        PerfilAcesso.objects.create(
            usuario=self.usuario_comum,
            role='Atendente',
            superusuario=False,
            admin_municipio=False,
            profissional_interno=True,
            usuario_externo=False,
            visualizar=True,
            editor=False,
            comentar=True,
            aprovar=False,
            assinar=False,
            exportar=False,
        )

    def test_usuario_autenticado_pode_ver_as_proprias_permissoes(self):
        self.client.force_authenticate(user=self.usuario_comum)
        response = self.client.get('/api/permissoes/minhas/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'comum@email.com')

    def test_apenas_admin_pode_listar_usuarios(self):
        self.client.force_authenticate(user=self.usuario_comum)
        response = self.client.get('/api/permissoes/usuarios/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/permissoes/usuarios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_pode_atualizar_permissoes_de_outro_usuario(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f'/api/permissoes/usuarios/{self.usuario_comum.id}/atualizar/',
            {
                'editor': True,
                'aprovar': True,
                'role': 'Gestor'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        perfil = PerfilAcesso.objects.get(usuario=self.usuario_comum)
        self.assertTrue(perfil.editor)
        self.assertTrue(perfil.aprovar)
        self.assertEqual(perfil.role, 'Gestor')

    def test_usuario_comum_nao_pode_atualizar_permissoes(self):
        self.client.force_authenticate(user=self.usuario_comum)

        response = self.client.patch(
            f'/api/permissoes/usuarios/{self.admin.id}/atualizar/',
            {
                'editor': True
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
