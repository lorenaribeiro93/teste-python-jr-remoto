from rest_framework import viewsets, status
from rest_framework.views import Response
from django.shortcuts import render, redirect


from api import models, serializers
from api.integrations.github import File, GithubApi
from api.integrations.file import *

# TODOS:
# 1 - Buscar organização pelo login através da API do Github
# 2 - Armazenar os dados atualizados da organização no banco
# 3 - Retornar corretamente os dados da organização
# 4 - Retornar os dados de organizações ordenados pelo score na listagem da API


class OrganizationViewSet(viewsets.ModelViewSet):

    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    lookup_field = "login"
    github_api = GithubApi()
    arquivo = File()

    def list(self, request, *args, **kwargs):
        return Response(self.arquivo.get_organizations())

    def retrieve(self, request, login=None):
        if request.method == 'GET':
            try:
                return Response(self.github_api.get_organization(login))
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, login=None):
        try:
            self.github_api.delete(login)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)