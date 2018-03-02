import string
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
import requests
from django.template.loader import render_to_string, get_template

from django.template import Context, Template
from django.core.mail import EmailMessage

from django.contrib.auth.models import User

from tacomseguro.models import CotacaoRequest, PhoneList, AddressInfos, Status

import xmltodict, json
from sinesp_client import SinespClient
import datetime

from celery import shared_task

@shared_task
def cotacao_task():
    status_pendente = Status.objects.get(name='pendente')
    status_cotado = Status.objects.get(name='cotado')
    cotacoes = None
    cotacoes = CotacaoRequest.objects.all()
    for c in cotacoes:
        if c.status == status_pendente:
            #""" CONSUMO SINESP """
            sc = SinespClient()
            print(c.placa)
            result = sc.search(c.placa)
            print(result)
            cotacao_request_update_1 = CotacaoRequest(id=c.id, cotacao_type=c.cotacao_type, email=c.email, cpf=c.cpf, placa=c.placa, cep=c.cep,  chassi=result['chassis'], modelo=result['model'], marca=result['brand'], anoFabricacao=result['year'], anoModelo=result['model_year'], date_created_at=datetime.date.today(), hour_created_at=datetime.datetime.now())
            print(cotacao_request_update_1.cpf)
            cotacao_request_update_1.save()
                    
            #""" CONSUMO BIPBOP """
            params = {'q': "USING 'CRAWLER' SELECT FROM 'FINDER'.'CONSULTA' WHERE 'DOCUMENTO'='{}'".format(cotacao_request_update_1.cpf), 'apiKey': 'e3dc8917fdb86bdf654bfd976696024b'}
            response = requests.post('https://irql.bipbop.com.br', params = params) 
            infos = xmltodict.parse(response.text)
            infos_json = json.dumps(infos)
            print(infos_json)

            if (infos['BPQL']['body']['xml']['ocorrencia']['codocor'] == '0'):

                print('encontrado')
                dados_cadastro = infos['BPQL']['body']['xml']['cadastro']
                            
                cotacao_request_update_2 = CotacaoRequest(id=cotacao_request_update_1.id, 
                cotacao_type=c.cotacao_type,
                email=c.email, 
                cpf=c.cpf, 
                placa=c.placa, 
                cep=c.cep, 
                chassi=result['chassis'], 
                modelo=result['model'], 
                marca=result['brand'], 
                anoFabricacao=result['year'], 
                anoModelo=result['model_year'], 
                nome_completo=dados_cadastro['nome'], 
                data_nascimento=dados_cadastro['dtnascimento'],
                sexo=dados_cadastro['sexo'],
                date_created_at=datetime.date.today(), 
                hour_created_at=datetime.datetime.now()
                )
                cotacao_request_update_2.save()

                #salvando telefones
                if (infos['BPQL']['body']['xml']['telefones']):
                    dados_telefone = infos['BPQL']['body']['xml']['telefones']['telefone']
                    if isinstance(infos['BPQL']['body']['xml']['telefones']['telefone'], list):
                        for i in range(len(dados_telefone)):
                            cotacao_request_update_3 = PhoneList(cotacao_id=cotacao_request_update_2.id, ddd=dados_telefone[i]['ddd'],  numero=dados_telefone[i]['numero'])
                            cotacao_request_update_3.save()
                    else:
                        cotacao_request_update_3 = PhoneList(cotacao_id=cotacao_request_update_2.id, ddd=dados_telefone['ddd'],  numero=dados_telefone['numero'])
                        cotacao_request_update_3.save()

                #salvando endereços
                if(infos['BPQL']['body']['xml']['enderecos']):
                    dados_endereco = infos['BPQL']['body']['xml']['enderecos']['endereco']            
                    if isinstance(infos['BPQL']['body']['xml']['enderecos']['endereco'], list):
                        for i in range(len(dados_endereco)):
                            cotacao_request_update_4 = AddressInfos(cotacao_id=cotacao_request_update_2.id, tipo=dados_endereco[i]['tipo'], logradouro=dados_endereco[i]['logradouro'], numero=dados_endereco[i]['numero'], bairro=dados_endereco[i]['bairro'], cidade=dados_endereco[i]['cidade'], estado=dados_endereco[i]['estado'], complemento=dados_endereco[i]['complemento'])
                            cotacao_request_update_4.save()
                    else:
                        cotacao_request_update_4 = AddressInfos(cotacao_id=cotacao_request_update_2.id, tipo=dados_endereco['tipo'], logradouro=dados_endereco['logradouro'], numero=dados_endereco['numero'], bairro=dados_endereco['bairro'], cidade=dados_endereco['cidade'], estado=dados_endereco['estado'], complemento=dados_endereco['complemento'])
                        cotacao_request_update_4.save()

                
                change_status = CotacaoRequest(id=c.id, 
                    status=status_cotado,
                )
                change_status.save(update_fields=["status"])  
                print('Cotacao concluida!!')   

            else:
                print('não encontrado')
                cotacao_request_update_2 = CotacaoRequest(id=cotacao_request_update_1.id, 
                cotacao_type=c.cotacao_type,
                email=c.email, 
                cpf=c.cpf, 
                placa=c.placa, 
                cep=c.cep, 
                chassi=result['chassis'], 
                modelo=result['model'], 
                marca=result['brand'], 
                anoFabricacao=result['year'], 
                anoModelo=result['model_year'],
                date_created_at=datetime.date.today(), 
                hour_created_at=datetime.datetime.now()
                )
                cotacao_request_update_2.save()

                change_status = CotacaoRequest(id=c.id, 
                    status=status_cotado,
                    )
                change_status.save(update_fields=["status"])  
                print('Cotacao concluida!!')   
    
            return Response({'status': 'OK'})
                    
            # #ENVIO DE EMAIL 
            # template = Template('cotacao.html')
            # print("email")
            # context = Context({
            #     'email': email,
            #     'cpf': cpf,
            #     'placa': placa,
            #     'cep': cep,
            # })

            # content = render_to_string('cotacao.html', {'context': context })
            # send_email = EmailMessage("Cotação de Seguro Carro: {}".format(placa), content , 'contato@tacomseguro.com', ['zeneto1@gmail.com'], reply_to=[email])
            # send_email.content_subtype = 'html'
            # send_email.send()
            # return Response({'status': 'OK'})  
    
    return Response( status = status.HTTP_200_OK)
    
