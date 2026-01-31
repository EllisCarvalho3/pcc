from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('alimentacao.urls')),
   path('accounts/', include('django.contrib.auth.urls')),
    path("perfil/", include("perfil.urls")),
    path("refeicoes/", include("refeicoes.urls")),
]
