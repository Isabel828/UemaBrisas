from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Processo
from .serializadores import ProcessoSerializer
from permissoes.permissoes import IsAdministrador


@api_view(["GET", "POST"])
def processos_view(request):

    # 🔍 GET → qualquer usuário pode ver
    if request.method == "GET":
        processos = Processo.objects.all().order_by("-created_at")
        serializer = ProcessoSerializer(processos, many=True)
        return Response(serializer.data)

    # 🔐 POST → só ADMIN pode criar
    if request.method == "POST":
        if not IsAdministrador().has_permission(request, None):
            return Response(
                {"erro": "Acesso negado. Apenas administradores podem criar processos."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProcessoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
