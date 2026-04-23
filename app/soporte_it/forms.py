from django import forms
from django.contrib.auth.models import User

from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}
            ),
        }


class TicketGestionForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['estado', 'tecnico_asignado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'tecnico_asignado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tecnico_asignado'].queryset = User.objects.filter(
            is_staff=True
        ).order_by('username')
        self.fields['tecnico_asignado'].required = False

