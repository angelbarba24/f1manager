# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Escuderia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Unicidad: no puede haber dos escuderías con el mismo nombre
    pais = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Circuito(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Unicidad: no puede haber dos circuitos con el mismo nombre
    pais = models.CharField(max_length=50)
    longitud_km = models.FloatField()
    vueltas = models.IntegerField()
    fecha = models.DateField()  # Necesario para la regla: no permitir predicciones en carreras finalizadas

    def __str__(self):
        return self.nombre


class Piloto(models.Model):
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()
    escuderia = models.ForeignKey(Escuderia, on_delete=models.PROTECT)  
    # PROTECT: no se puede borrar una escudería si tiene pilotos asociados

    pais = models.CharField(max_length=50)

    class Meta:
        unique_together = ('nombre', 'numero')  
        # Unicidad: no puede haber dos pilotos con el mismo nombre y número

    def __str__(self):
        return f"{self.nombre} ({self.numero})"


class Favorito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    piloto = models.ForeignKey(Piloto, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'piloto')  
        # Regla: un usuario no puede marcar dos veces el mismo piloto como favorito

    def __str__(self):
        return f"{self.user.username} → {self.piloto.nombre}"


class Prediccion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    circuito = models.ForeignKey(Circuito, on_delete=models.CASCADE)
    primero = models.ForeignKey(Piloto, on_delete=models.CASCADE, related_name='prediccion_primero')
    segundo = models.ForeignKey(Piloto, on_delete=models.CASCADE, related_name='prediccion_segundo')
    tercero = models.ForeignKey(Piloto, on_delete=models.CASCADE, related_name='prediccion_tercero')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'circuito')  
        # Regla: un usuario no puede hacer dos predicciones para la misma carrera

    def clean(self):
        # Regla: no se pueden crear predicciones para carreras ya finalizadas
        if self.circuito.fecha < timezone.now().date():
            raise ValidationError("No se pueden crear predicciones para carreras ya finalizadas.")

    def __str__(self):
        return f"Predicción de {self.user.username} en {self.circuito.nombre}"