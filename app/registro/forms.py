from django import forms

from academico.models import ExpedienteEstudiante

from .models import CicloAcademico, Inscripcion


class CicloAcademicoForm(forms.ModelForm):
    class Meta:
        model = CicloAcademico
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'fecha_fin': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['materia', 'ciclo']
        widgets = {
            'materia': forms.Select(attrs={'class': 'form-select'}),
            'ciclo': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ciclo'].queryset = CicloAcademico.objects.filter(
            activo=True
        ).order_by('-fecha_inicio')


class InscripcionGestionForm(forms.ModelForm):
    expediente = forms.ModelChoiceField(
        queryset=ExpedienteEstudiante.objects.select_related('usuario').order_by(
            'carnet'
        ),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Inscripcion
        fields = ['expediente', 'materia', 'ciclo']
        widgets = {
            'materia': forms.Select(attrs={'class': 'form-select'}),
            'ciclo': forms.Select(attrs={'class': 'form-select'}),
        }

