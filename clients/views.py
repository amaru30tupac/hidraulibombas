from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClientForm
from .models import Client


@login_required
def client_list_view(request):
    query = request.GET.get("q", "").strip()

    clients = Client.objects.all()

    if query:
        clients = clients.filter(name__icontains=query)

    context = {
        "page_title": "Clientes",
        "clients": clients,
        "query": query,
    }
    return render(request, "clients/client_list.html", context)


@login_required
def client_create_view(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente creado correctamente.")
            return redirect("client_list")
    else:
        form = ClientForm()

    return render(request, "clients/client_form.html", {
        "page_title": "Crear cliente",
        "form": form,
        "form_title": "Crear cliente",
    })


@login_required
def client_update_view(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect("client_list")
    else:
        form = ClientForm(instance=client)

    return render(request, "clients/client_form.html", {
        "page_title": "Editar cliente",
        "form": form,
        "form_title": f"Editar cliente: {client.name}",
    })


@login_required
def client_delete_view(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client.delete()
        messages.success(request, "Cliente eliminado correctamente.")
        return redirect("client_list")

    return render(request, "clients/client_confirm_delete.html", {
        "page_title": "Eliminar cliente",
        "client": client,
    })