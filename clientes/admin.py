from django.contrib import admin
from .actions import emitir_nfe, reverter_nfe
from .models import Person, Documento, Venda, Produto

class PersonAdmin(admin.ModelAdmin):
    # Vc pode incluir os campos que vc quer ver na edição
    # fields = (('first_name', 'last_name'), ('age','salary'), 'bio','doc','photo')
    # ou excluir os campos que vc quer ver na edição
    # exclude = ('bio',)

    # caso queira agrupar de forma diferente
    fieldsets = (
        ('Nome', {
            'fields': (('first_name', 'last_name'),)
        }),
        ('Dados Básicos', {
            'fields': ('age','salary','doc')
        }),
        ('Dados Complementares', {
            'classes': ('collapse',),
            'fields':('bio','photo')
        }),
    )
    
    #para exibir os campos que vc quer ver na listagem
    list_display = ('nome_completo', 'doc','tem_foto')
    #para exibir filtros de pesquisa
    list_filter = ('age','salary','doc')
    search_fields = ('id','first_name','last_name')
    autocomplete_fields = ['doc']

    def tem_foto(self, obj):
        if obj.photo:
            return 'Sim'
        else:
            return 'Não'
    tem_foto.short_description = 'Possui foto'


class VendaAdmin(admin.ModelAdmin):
    list_filter = ('pessoa__doc','desconto')
    # raw_id_fields = ('pessoa',) <<< Faz a busca como a tela de CRUD de Admin
    autocomplete_fields = ['pessoa']
    readonly_fields = ('valor',)
    list_display = ('numero', 'valor','total','nfe_emitida','emitiu_nf')
    search_fields = ('numero','pessoa__first_name', 'pessoa__last_name','pessoa__doc__num_doc')
    actions = [emitir_nfe, reverter_nfe]
    filter_horizontal =['produtos',]

    def total(self, obj):
        return obj.get_total()

    total.short_description = 'total'

    def emitiu_nf(self, obj):
        if obj.nfe_emitida:
            return 'Sim'
        else:
            return 'Não'
    emitiu_nf.short_description = 'Emitiu NF?'



class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'preco')


class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('num_doc',)
    search_fields = ('num_doc',)

admin.site.register(Person, PersonAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Venda, VendaAdmin)
admin.site.register(Produto, ProdutoAdmin)

admin.site.site_header = 'Gestão de Clientes'
admin.site.index_title = 'Administração'
admin.site.site_title = 'Seja bem vindo ao Gestão de Clientes'
