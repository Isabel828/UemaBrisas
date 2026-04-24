from django.urls import path

from .views import (
    minhas_permissoes,
    minhas_regras,  # 🔥 NOVO
    listar_usuarios_permissoes,
    detalhar_permissoes_usuario,
    atualizar_permissoes_usuario,
    listar_regras_disponiveis,
)

urlpatterns = [
    path('minhas/', minhas_permissoes, name='minhas-permissoes'),

    # 🔥 ENDPOINT QUE O FRONTEND DEVE USAR
    path('minhas-regras/', minhas_regras, name='minhas-regras'),

    path('usuarios/', listar_usuarios_permissoes, name='listar-usuarios-permissoes'),
    path('usuarios/<int:usuario_id>/', detalhar_permissoes_usuario, name='detalhar-permissoes-usuario'),
    path('usuarios/<int:usuario_id>/atualizar/', atualizar_permissoes_usuario, name='atualizar-permissoes-usuario'),

    path('regras/', listar_regras_disponiveis, name='listar-regras-disponiveis'),
]