from django.db import models
from django.contrib.auth.models import User


class PerfilAcesso(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Tecnico', 'Tecnico'),
        ('Juridico', 'Juridico'),
        ('Atendente', 'Atendente'),
        ('Gestor', 'Gestor'),
        ('Auditor', 'Auditor'),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_acesso'
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='Atendente')

    superusuario = models.BooleanField(default=False)
    admin_municipio = models.BooleanField(default=False)
    profissional_interno = models.BooleanField(default=True)
    usuario_externo = models.BooleanField(default=False)

    visualizar = models.BooleanField(default=True)
    editor = models.BooleanField(default=False)
    comentar = models.BooleanField(default=True)
    aprovar = models.BooleanField(default=False)
    assinar = models.BooleanField(default=False)
    exportar = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de acesso'
        verbose_name_plural = 'Perfis de acesso'

    def __str__(self):
        return f'{self.usuario.username} - {self.role}'
