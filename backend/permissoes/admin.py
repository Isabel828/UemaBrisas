from django.contrib import admin
from .models import PerfilAcesso


@admin.register(PerfilAcesso)
class PerfilAcessoAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'role',
        'superusuario',
        'admin_municipio',
        'profissional_interno',
        'usuario_externo',
    )
    search_fields = ('usuario__username', 'usuario__email')
    list_filter = (
        'role',
        'superusuario',
        'admin_municipio',
        'profissional_interno',
        'usuario_externo',
    )
