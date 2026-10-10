from django.shortcuts import render, redirect
from .models import Item
from .forms import ItemForm

def gerenciar_estoque(request):
    # Se o usuário enviou o formulário (clicou em salvar)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save() # Salva direto no banco de dados (CREATE)
            return redirect('estoque') # Recarrega a página para limpar o formulário
    
    # Se o usuário apenas acessou a página (GET)
    else:
        form = ItemForm() # Cria um formulário vazio

    # Busca todos os produtos para a tabela (READ)
    itens = Item.objects.all()

    # Envia o formulário e a lista de produtos para o HTML
    contexto = {
        'form': form,
        'itens': itens
    }
    return render(request, 'estoque.html', contexto)