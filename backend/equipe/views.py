from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
def aprovar_cargo(request):
    return Response(
        {"mensagem": "Cargo aprovado com sucesso!"},
        status=status.HTTP_200_OK
    )