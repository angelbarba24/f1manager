# Register your models here.

from django.contrib import admin
from .models import Piloto, Escuderia, Circuito


@admin.register(Piloto)
class PilotoAdmin(admin.ModelAdmin):
    readonly_fields = ('nombre', 'numero', 'escuderia', 'pais')

@admin.register(Escuderia)
class EscuderiaAdmin(admin.ModelAdmin):
    readonly_fields = ('nombre', 'pais')


@admin.register(Circuito)
class CircuitoAdmin(admin.ModelAdmin):
    readonly_fields = ('nombre', 'pais', 'longitud_km', 'vueltas', 'fecha')