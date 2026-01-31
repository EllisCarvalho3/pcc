from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Perfil
from .forms import PerfilForm
from .services import calcular_meta

@login_required
def perfil_view(request):
    perfil, created = Perfil.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            perfil = form.save(commit=False)

            perfil.meta_calorica = calcular_meta(
                perfil.peso,
                perfil.altura,
                perfil.idade,
                perfil.atividade,
                perfil.objetivo
            )

            perfil.save()
            return redirect("dashboard")
    else:
        form = PerfilForm(instance=perfil)

    return render(request, "perfil/perfil.html", {"form": form})
