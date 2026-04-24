from django.contrib.auth.models import User
from rest_framework import serializers

from .models import PerfilAcesso


class UsuarioResumoSerializador(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'name', 'is_active']

    def get_name(self, obj):
        nome = f'{obj.first_name} {obj.last_name}'.strip()
        return nome or obj.username


class PerfilAcessoSerializador(serializers.ModelSerializer):
    usuario = UsuarioResumoSerializador(read_only=True)

    class Meta:
        model = PerfilAcesso
        fields = [
            'id',
            'usuario',
            'role',
            'superusuario',
            'admin_municipio',
            'profissional_interno',
            'usuario_externo',
            'visualizar',
            'editor',
            'comentar',
            'aprovar',
            'assinar',
            'exportar',
            'criado_em',
            'atualizado_em',
        ]

    def validate(self, attrs):
        usuario_externo = attrs.get('usuario_externo', getattr(self.instance, 'usuario_externo', False))
        profissional_interno = attrs.get('profissional_interno', getattr(self.instance, 'profissional_interno', True))
        superusuario = attrs.get('superusuario', getattr(self.instance, 'superusuario', False))
        admin_municipio = attrs.get('admin_municipio', getattr(self.instance, 'admin_municipio', False))

        if usuario_externo and profissional_interno:
            raise serializers.ValidationError(
                'Um usuario nao pode ser externo e profissional interno ao mesmo tempo.'
            )

        if superusuario:
            attrs['admin_municipio'] = True
            attrs['profissional_interno'] = True
            attrs['usuario_externo'] = False

        if admin_municipio:
            attrs['profissional_interno'] = True
            attrs['usuario_externo'] = False

        return attrs


class AtualizarPerfilAcessoSerializador(serializers.ModelSerializer):
    class Meta:
        model = PerfilAcesso
        fields = [
            'role',
            'superusuario',
            'admin_municipio',
            'profissional_interno',
            'usuario_externo',
            'visualizar',
            'editor',
            'comentar',
            'aprovar',
            'assinar',
            'exportar',
        ]

    def validate(self, attrs):
        usuario_externo = attrs.get('usuario_externo', getattr(self.instance, 'usuario_externo', False))
        profissional_interno = attrs.get('profissional_interno', getattr(self.instance, 'profissional_interno', True))
        superusuario = attrs.get('superusuario', getattr(self.instance, 'superusuario', False))
        admin_municipio = attrs.get('admin_municipio', getattr(self.instance, 'admin_municipio', False))

        if usuario_externo and profissional_interno:
            raise serializers.ValidationError(
                'Um usuario nao pode ser externo e profissional interno ao mesmo tempo.'
            )

        if superusuario:
            attrs['admin_municipio'] = True
            attrs['profissional_interno'] = True
            attrs['usuario_externo'] = False

        if admin_municipio:
            attrs['profissional_interno'] = True
            attrs['usuario_externo'] = False

        return attrs
