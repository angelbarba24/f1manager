from django import forms
from .models import Prediccion, Circuito
from datetime import date

class PrediccionForm(forms.ModelForm):
    class Meta:
        model = Prediccion
        fields = ['circuito', 'primero', 'segundo', 'tercero']
        widgets = {
            'circuito': forms.Select(attrs={'class': 'form-select'}),
            'primero': forms.Select(attrs={'class': 'form-select'}),
            'segundo': forms.Select(attrs={'class': 'form-select'}),
            'tercero': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'primero': '🥇 Ganador',
            'segundo': '🥈 Segundo Lugar',
            'tercero': '🥉 Tercer Lugar',
        }

    def __init__(self, *args, **kwargs):
        # Extraemos el usuario que pasaremos desde la vista
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtramos carreras futuras
        circuitos_futuros = Circuito.objects.filter(fecha__gte=date.today()).order_by('fecha')
        
        # Si estamos creando una NUEVA predicción (no editando), quitamos las que ya tienen predicción
        if self.user and not self.instance.pk:
            carreras_jugadas = Prediccion.objects.filter(user=self.user).values_list('circuito_id', flat=True)
            circuitos_futuros = circuitos_futuros.exclude(id__in=carreras_jugadas)
            
        self.fields['circuito'].queryset = circuitos_futuros
        
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('primero')
        p2 = cleaned_data.get('segundo')
        p3 = cleaned_data.get('tercero')

        if p1 and p2 and p3:
            if p1 == p2 or p1 == p3 or p2 == p3:
                raise forms.ValidationError("¡No puedes repetir el mismo piloto en el podio!")