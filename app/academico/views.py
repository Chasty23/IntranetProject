from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Nota

@login_required
@permission_required('academico.view_nota', raise_exception=True)
def lista_notas(request):
    # Todos los usuarios autenticados pueden ver las notas (Nivel Consulta) [cite: 71]
    notas = Nota.objects.all()
    return render(request, 'academico/notas.html', {'notas': notas})

@permission_required('academico.puede_modificar_notas', raise_exception=True)
def editar_nota(request, nota_id):
    # Si alguien de 'Consulta' intenta entrar, Django dará error 403 [cite: 93]
    nota = get_object_or_404(Nota, id=nota_id)
    if request.method == 'POST':
        nueva_nota = request.POST.get('calificacion')
        nota.calificacion = nueva_nota
        nota.save()
        return redirect('lista_notas')
    
    return render(request, 'academico/editar.html', {'nota': nota})
