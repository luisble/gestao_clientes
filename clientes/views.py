from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Person, Produto, Venda
from .forms import PersonForm

@login_required
def persons_list(request):
    persons = Person.objects.all()
    return render(request, 'person.html', {'persons': persons,})


@login_required
def persons_new(request):
    form = PersonForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('person_list')
    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_update(request, id):
    person = get_object_or_404(Person, pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if form.is_valid():
        form.save()
        return redirect('person_list')

    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_delete(request, id):
    person = get_object_or_404(Person, pk=id)

    if request.method == 'POST':
        person.delete()
        return redirect('person_list')

    return render(request, 'person_delete_confirm.html', {'person': person})


class PersonList(ListView):
    model = Person
    # se vc não quiser colocar o nome do template, o django vai procurar pelo nome do model, mais underline,
    # mais list.html. No nosso exemplo person_list.html

class PersonDetailView(DetailView):

    model = Person

    #Reescreveu o Get object incluindo o Select Related 
    def get_object(self, querset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return Person.objects.select_related('doc').get(id=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['vendas'] = Venda.objects.filter(pessoa_id=self.object.id)
        return context

class PersonCreate(CreateView):

    model = Person
    fields = ['first_name','last_name', 'age', 'salary', 'bio','photo']
    
    # você pode chamar definir a variável success_url ou 
    # caso queira fazer algo antes, vc pode definir a função
    # get_success_url e vc define para onde quer enviar a página
    #success_url = reverse_lazy('person_list_cbv')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funcao'] = 'Incluir Cliente'
        return context

class PersonUpdate(UpdateView):

    model = Person
    fields = ['first_name','last_name', 'age', 'salary', 'bio','photo']
    
    def get_success_url(self):
        return reverse_lazy('person_list_cbv')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funcao'] = 'Atualizar Cliente'
        return context


class PersonDelete(DeleteView):

    model = Person
    def get_success_url(self):
        return reverse_lazy('person_list_cbv')

def home(request):
    return render(request, 'clientes/home.html')

class ProdutoBulk(View):
    def get(self, request):
        produtos = ['Banana', 'Maçã', 'Limão', 'Laranja', 'Abacaxi', 'Ameixa','Pera','Melancia']
        list_produtos = []

        for produto in produtos:
            p = Produto(descricao=produto, preco=10)
            list_produtos.append(p)
        
        Produto.objects.bulk_create(list_produtos)
        return render(request, 'clientes/home.html')

@receiver(m2m_changed, sender=Venda.produtos.through)
def update_vendas_total(sender,instance,**kwargs):
    instance.valor = instance.get_total()
    instance.save()
    # ou poderia utilizar como abaixo...
    # total = instance.get_total()
    # Venda.objects.filter(id=instance.id).update(valor=total)