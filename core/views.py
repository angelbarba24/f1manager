from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Piloto, Circuito, Escuderia
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from .forms import PrediccionForm
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from datetime import date
from .models import Piloto, Circuito, Escuderia, Prediccion, Favorito
from .forms import PrediccionForm

# 1. VISTA DEL DASHBOARD (HOME)
@login_required
def home(request):
    # Datos generales
    total_pilotos = Piloto.objects.count()
    total_equipos = Escuderia.objects.count()
    total_circuitos = Circuito.objects.count()
    
    # Buscar la próxima carrera
    proxima_carrera = Circuito.objects.filter(fecha__gte=date.today()).order_by('fecha').first()
    
    dias_restantes = None
    numero_carrera = 0

    if proxima_carrera:
        # Calcular días restantes
        delta = proxima_carrera.fecha - date.today()
        dias_restantes = delta.days
        
        # Calcular número de carrera
        numero_carrera = Circuito.objects.filter(fecha__lte=proxima_carrera.fecha).count()
    
    context = {
        'total_pilotos': total_pilotos,
        'total_equipos': total_equipos,
        'proxima_carrera': proxima_carrera,
        'dias_restantes': dias_restantes,
        'numero_carrera': numero_carrera,
        'total_circuitos': total_circuitos
    }
    return render(request, 'core/home.html', context)

# 2. VISTA DE LA PARRILLA
@login_required
def parrilla_2026(request):
    pilotos = Piloto.objects.select_related('escuderia').all().order_by('escuderia__nombre', 'numero')
    
    # Obtenemos los IDs de los pilotos que el usuario ya tiene como favoritos
    lista_favoritos_ids = Favorito.objects.filter(user=request.user).values_list('piloto_id', flat=True)
    
    return render(request, 'core/parrilla.html', {
        'pilotos': pilotos,
        'lista_favoritos_ids': lista_favoritos_ids
    })

# 3. VISTA DEL CALENDARIO
@login_required
def calendario_2026(request):
    circuitos = Circuito.objects.all().order_by('fecha')
    return render(request, 'core/calendario.html', {'circuitos': circuitos})

# 4. VISTAS DE PREDICCIONES
@login_required
def crear_prediccion(request):
    if request.method == 'POST':
        # Le pasamos el user al formulario
        form = PrediccionForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                prediccion = form.save(commit=False)
                prediccion.user = request.user
                prediccion.save()
                messages.success(request, '¡Predicción guardada con éxito!')
                return redirect('lista_predicciones')
            except IntegrityError:
                messages.error(request, 'Ya has hecho una predicción para este circuito.')
    else:
        form = PrediccionForm(user=request.user) # Pasamos el user aquí también

    return render(request, 'core/crear_prediccion.html', {'form': form, 'editando': False})

@login_required
def lista_predicciones(request):
    # Traemos las predicciones del usuario, ordenadas por la fecha del circuito
    predicciones = Prediccion.objects.filter(user=request.user).select_related('circuito').order_by('circuito__fecha')
    return render(request, 'core/lista_predicciones.html', {'predicciones': predicciones, 'hoy': date.today()})

@login_required
def editar_prediccion(request, pk):
    # Buscamos la predicción. Aseguramos que sea de este usuario
    prediccion = get_object_or_404(Prediccion, pk=pk, user=request.user)
    
    # Validamos que no se puedan editar carreras pasadas o en curso
    if prediccion.circuito.fecha <= date.today():
        messages.error(request, "La carrera ya ha comenzado o finalizado. No se puede modificar.")
        return redirect('lista_predicciones')

    if request.method == 'POST':
        form = PrediccionForm(request.POST, instance=prediccion, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Predicción actualizada con éxito.')
            return redirect('lista_predicciones')
    else:
        form = PrediccionForm(instance=prediccion, user=request.user)

    return render(request, 'core/crear_prediccion.html', {'form': form, 'editando': True})

@login_required
def borrar_prediccion(request, pk):
    prediccion = get_object_or_404(Prediccion, pk=pk, user=request.user)
    
    if prediccion.circuito.fecha <= date.today():
        messages.error(request, "No puedes borrar predicciones de carreras pasadas.")
        return redirect('lista_predicciones')

    if request.method == 'POST':
        prediccion.delete()
        messages.success(request, 'Predicción eliminada.')
        return redirect('lista_predicciones')
        
    return render(request, 'core/borrar_prediccion.html', {'prediccion': prediccion})

# 5. VISTA FAVORITOS
@login_required
def toggle_favorito(request, piloto_id):
    piloto = get_object_or_404(Piloto, id=piloto_id)
    # Buscamos si ya existe el favorito
    favorito, created = Favorito.objects.get_or_create(user=request.user, piloto=piloto)
    
    if not created:
        # Si ya existía, lo borramos (desmarcar)
        favorito.delete()
        messages.info(request, f"{piloto.nombre} eliminado de favoritos.")
    else:
        messages.success(request, f"{piloto.nombre} añadido a favoritos.")
    
    # Volvemos a la página donde estábamos
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def mis_favoritos(request):
    favoritos = Favorito.objects.filter(user=request.user).select_related('piloto', 'piloto__escuderia')
    return render(request, 'core/mis_favoritos.html', {'favoritos': favoritos})