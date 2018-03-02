from django.contrib.auth.models import User, Group
from rest_framework import serializers
from tacomseguro.models import CotacaoRequest, Status, PhoneList, AddressInfos

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
        
class PhoneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneList
        fields = ['ddd', 'numero']

class AddressInfosSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressInfos
        fields = ['tipo', 'logradouro', 'numero', 'bairro', 'cidade', 'estado', 'complemento']

class CotacaoRequestSerializer(serializers.ModelSerializer):    
    phonelist = PhoneListSerializer(many=True, read_only=True)
    addressinfos = AddressInfosSerializer(many=True, read_only=True)
    class Meta:
        model = CotacaoRequest
        fields = ('id', 'status', 'cotacao_type', 'email', 'cpf', 'placa', 'cep', 'chassi', 'modelo', 'marca', 'anoFabricacao', 'anoModelo', 'nome_completo', 'estado_civil', 'data_nascimento', 'sexo', 'celular', 'hour_created_at', 'date_created_at', 'phonelist', 'addressinfos')

