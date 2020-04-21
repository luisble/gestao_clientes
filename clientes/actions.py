# Neste exemplo, usou o próprio update, pois é mais performático
def emitir_nfe(modeladmin, request, queryset):
    rows_updated = queryset.update(nfe_emitida=True)
    if rows_updated == 1:
        message_bit = "1 Venda com "
    else:
        message_bit = "%s  Vendas com " % rows_updated
    modeladmin.message_user(request, "%s nota(s) emitida(s) com sucesso." % message_bit)
emitir_nfe.short_description = "Marcar vendas com NF-e emitida"

# Neste outro exemplo, usamos o for para o caso de querer fazer
# mais ações. Exemplo: Chamar um método antes.
def reverter_nfe(modeladmin, request, queryset):
    for obj in queryset:
        obj.nfe_emitida=False
        obj.save()
    rows_updated = len(queryset)
    if rows_updated == 1:
        message_bit = "1 Venda com "
    else:
        message_bit = "%s  Vendas com " % rows_updated
    modeladmin.message_user(request, "%s nota(s) revertida(s) com sucesso." % message_bit)
reverter_nfe.short_description = "Marcar vendas com NF-e não emitida"