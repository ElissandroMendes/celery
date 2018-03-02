from django.db import models
import datetime


class Status(models.Model):
    name = models.CharField(verbose_name="Nome", db_column='name', max_length=50, blank=False, null=False)

    class Meta:
        db_table = 'status'
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Status, self).save(*args, **kwargs)

class CotacaoRequest(models.Model):

    GENDER_CHOICES = (
        ('1', 'Masculino'),
        ('2', 'Feminino'),
    )
    CIVILSTATUS_CHOICES = (
        ('SOLTERIRO', 'Solteiro'),
        ('CASADO', 'Casado'),
    )
    COTACAOTYPE_CHOICES = (
        ('AUTO', 'Auto'),
        ('VIAGEM', 'Viagem'),
        ('INCENDIO', 'Incendio'),
        ('VIDA', 'Vida')
    )
    cotacao_type= models.CharField(verbose_name='Tipo de Cotação', choices=COTACAOTYPE_CHOICES, max_length=200, blank=False, null=True) 
    email= models.CharField(verbose_name='Email', max_length=200, blank=False, null=False)
    cpf= models.CharField(verbose_name='CPF', max_length=14, blank=False, null=False)
    placa= models.CharField(verbose_name='Número de placa', max_length=200, blank=False, null=False)
    cep= models.CharField(verbose_name='Cep', max_length=9, blank=False, null=False)
    date_created_at= models.DateField(verbose_name='Data de solicitação', editable=False, blank=True, null=True)
    hour_created_at= models.TimeField(verbose_name='Hora de solicitação', editable=False, blank=True, null=True)
    chassi= models.CharField(verbose_name='Chassi', max_length=200, blank=False, null=True)
    modelo= models.CharField(verbose_name='Modelo', max_length=200, blank=False, null=True)
    marca= models.CharField(verbose_name='Marca', max_length=200, blank=False, null=True)
    anoFabricacao= models.CharField(verbose_name='Ano de Fabricação', max_length=200, blank=False, null=True)
    anoModelo= models.CharField(verbose_name='Ano de Modelo', max_length=200, blank=False, null=True)
    nome_completo= models.CharField(verbose_name='Nome completo', max_length=200, blank=False, null=True)
    estado_civil= models.CharField(verbose_name='Estado Civil', choices=CIVILSTATUS_CHOICES, max_length=200, blank=False, null=True)
    data_nascimento= models.CharField(verbose_name='Data de nascimento', max_length=200, blank=False, null=True)
    sexo= models.CharField(verbose_name='Sexo',  choices=GENDER_CHOICES, max_length=200, blank=False, null=True)
    celular= models.CharField(verbose_name='Celular', max_length=200, blank=False, null=True)

    status= models.ForeignKey(Status, verbose_name='Status', db_column='status', null=True, blank=True)

    class Meta:
        db_table= "CotacaoRequest"
        verbose_name= "Pedido de Cotação"
        verbose_name_plural= 'Pedidos de Cotação'

class AddressInfos(models.Model):
    cotacao=models.ForeignKey(CotacaoRequest, verbose_name='Pedido de Cotação', related_name="AddressInfos", blank=False, null=True)
    tipo= models.CharField(verbose_name='Tipo', max_length=200, blank=False, null=True)
    logradouro= models.CharField(verbose_name='Logradouro', max_length=200, blank=False, null=True)
    numero= models.CharField(verbose_name='Numero', max_length=200, blank=False, null=True)
    bairro= models.CharField(verbose_name='Bairro', max_length=200, blank=False, null=True)
    cidade= models.CharField(verbose_name='Cidade', max_length=200, blank=False, null=True)
    estado= models.CharField(verbose_name='Estado', max_length=200, blank=False, null=True)
    complemento= models.CharField(verbose_name='Complemento', max_length=200, blank=False, null=True)
    class Meta:
        db_table= "AddressInfos"
        verbose_name= "Endereço"
        verbose_name_plural= 'Endereços'

    def __str__(self):
        return ''

class PhoneList(models.Model):
    cotacao=models.ForeignKey(CotacaoRequest, verbose_name='Pedido de Cotação', related_name="PhoneList", blank=False, null=True)
    ddd= models.CharField(verbose_name='DDD', max_length=900, db_column='DDD', blank=False, null=True)
    numero= models.CharField(verbose_name='Telefone', max_length=900, db_column='Telefone')

    class Meta:
        db_table= "PhoneList"
        verbose_name= "Telefone"
        verbose_name_plural= 'Telefones'