from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Perfil
from .forms import PerfilForm

@login_required
def perfil_view(request):
    perfil, created = Perfil.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = PerfilForm(instance=perfil)

    return render(request, "perfil/perfil.html", {"form": form})

