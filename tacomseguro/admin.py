from django.contrib import admin
from django.forms import ModelForm, TextInput, Textarea

from suit_ckeditor.widgets import CKEditorWidget

from tacomseguro.models import CotacaoRequest, Status, PhoneList, AddressInfos

class CotacaoForm(ModelForm):
    class Meta:
        widgets = {
            'nome_completo': TextInput(attrs={'class': 'span10'}),
            'email': TextInput(attrs={'class': 'span10'}),
	    }

class AddressForm(ModelForm):
    class Meta:
        widgets = {
            'logradouro': TextInput(attrs={'class': 'span10'}),
            'numero': TextInput(attrs={'class': 'span4'}),
	    }

class PhoneListInLine(admin.TabularInline):
    fieldsets = [
        ('Telefones', {'fields':['ddd', 'numero', 'cotacao']})
    ]
    model = PhoneList
    extra = 0

class AddressInfosInLine(admin.StackedInline):

    model = AddressInfos
    extra = 0
    form = AddressForm

class CotacaoRequestAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Status da Cotação', {'fields': ['status']}),
        ('Tipo de Cotação', {'fields': ['cotacao_type']}),
        ('Dados Pessoais', {'fields': ['nome_completo', 'email', ('data_nascimento', 'cpf') , 'estado_civil', 'sexo']}),
        ('Veiculo', {'fields': [('modelo', 'marca'), ('placa', 'chassi'), 'anoFabricacao', 'anoModelo']})
    ]

    list_display = [ 'email', 'nome_completo', 'cpf', 'placa', 'status', 'date_created_at', 'hour_created_at']
    search_fields = ['nome_completo', 'cpf', 'placa']
    form = CotacaoForm
    
    inlines = [AddressInfosInLine, PhoneListInLine]

class StatusAdmin(admin.ModelAdmin):
    pass

admin.site.register(Status, StatusAdmin)
admin.site.register(CotacaoRequest, CotacaoRequestAdmin)

# Register your models here.
