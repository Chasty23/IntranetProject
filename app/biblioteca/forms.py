from django import forms

from academico.models import ExpedienteEstudiante

from .models import Libro, Prestamo


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = [
            'titulo',
            'autor',
            'isbn',
            'ejemplares_totales',
            'ejemplares_disponibles',
            'activo',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'ejemplares_totales': forms.NumberInput(attrs={'class': 'form-control'}),
            'ejemplares_disponibles': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libro', 'fecha_prestamo', 'fecha_devolucion']
        widgets = {
            'libro': forms.Select(attrs={'class': 'form-select'}),
            'fecha_prestamo': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'fecha_devolucion': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['libro'].queryset = Libro.objects.filter(
            activo=True, ejemplares_disponibles__gt=0
        ).order_by('titulo')


class PrestamoGestionForm(forms.ModelForm):
    expediente = forms.ModelChoiceField(
        queryset=ExpedienteEstudiante.objects.select_related('usuario').order_by(
            'carnet'
        ),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Prestamo
        fields = ['expediente', 'libro', 'fecha_prestamo', 'fecha_devolucion', 'estado']
        widgets = {
            'libro': forms.Select(attrs={'class': 'form-select'}),
            'fecha_prestamo': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'fecha_devolucion': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

