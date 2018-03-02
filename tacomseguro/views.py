from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.request import Request

import requests
from django.template.loader import render_to_string, get_template

from django.template import Context, Template
from django.core.mail import EmailMessage

from tacomseguro.tasks import cotacao_task
from tacomseguro.models import CotacaoRequest, PhoneList, AddressInfos, Status
from tacomseguro.serializers import UserSerializer, GroupSerializer, PhoneListSerializer, AddressInfosSerializer, CotacaoRequestSerializer
import xmltodict, json

from sinesp_client import SinespClient
import datetime

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CotacaoRequestViewSet(viewsets.ModelViewSet):

    queryset = CotacaoRequest.objects.all()
    serializer_class = CotacaoRequestSerializer

    @list_route(methods=['post'], url_path='SendCotacaoRequest', url_name='SendCotacaoRequest')
    
    def ReceivingCotacaoRequest(self, request):
        cotacao_type = request.data['cotacao_type']
        email = request.data['email']
        cpf = request.data['cpf']
        placa = request.data['placa']
        cep = request.data['cep']

        if(email is not None and cpf is not None and placa is not None and cep is not None):    
            status_pendente = Status.objects.get(name='pendente')
            cotacao_request = None
          
            cotacao_request = CotacaoRequest(cotacao_type=cotacao_type, email=email, cpf=cpf, placa=placa, cep=cep, date_created_at=datetime.date.today(), hour_created_at=datetime.datetime.now(), status=status_pendente)
            cotacao_request.save()
           
            return Response( status = status.HTTP_200_OK)
    
class PhoneListViewSet(viewsets.ModelViewSet):
    queryset = PhoneList.objects.all()
    serializer_class = PhoneListSerializer

class AddressInfosViewSet(viewsets.ModelViewSet):
    queryset = AddressInfos.objects.all()
    serializer_class = AddressInfosSerializer