from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from academico.models import ExpedienteEstudiante

from .forms import LibroForm, PrestamoForm, PrestamoGestionForm
from .models import Libro, Prestamo


def puede_ver_prestamo(usuario, prestamo):
    return (
        usuario.is_superuser
        or usuario.has_perm('biblioteca.puede_gestionar_biblioteca')
        or prestamo.expediente.usuario == usuario
    )


@login_required
def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'biblioteca/lista_libros.html', {'libros': libros})


@login_required
def lista_prestamos(request):
    if request.user.is_superuser or request.user.has_perm(
        'biblioteca.puede_gestionar_biblioteca'
    ):
        prestamos = Prestamo.objects.select_related(
            'libro', 'expediente__usuario'
        ).all()
    else:
        prestamos = Prestamo.objects.select_related(
            'libro', 'expediente__usuario'
        ).filter(expediente__usuario=request.user)

    return render(
        request,
        'biblioteca/lista_prestamos.html',
        {'prestamos': prestamos},
    )


@login_required
def crear_prestamo(request):
    if request.user.is_superuser or request.user.has_perm(
        'biblioteca.puede_gestionar_biblioteca'
    ):
        form_class = PrestamoGestionForm
        expediente = None
    else:
        expediente = ExpedienteEstudiante.objects.filter(usuario=request.user).first()
        if expediente is None:
            messages.error(
                request,
                'Tu usuario no tiene expediente academico vinculado.',
            )
            return redirect('lista_prestamos_biblioteca')
        form_class = PrestamoForm

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            if expediente is not None:
                prestamo.expediente = expediente
            if prestamo.libro.ejemplares_disponibles <= 0:
                form.add_error('libro', 'No hay ejemplares disponibles para este libro.')
            else:
                prestamo.save()
                prestamo.libro.ejemplares_disponibles -= 1
                prestamo.libro.save(update_fields=['ejemplares_disponibles'])
                return redirect('lista_prestamos_biblioteca')
    else:
        form = form_class()

    return render(request, 'biblioteca/form_prestamo.html', {'form': form})


@login_required
def detalle_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(
        Prestamo.objects.select_related('libro', 'expediente__usuario'),
        id=prestamo_id,
    )
    if not puede_ver_prestamo(request.user, prestamo):
        return HttpResponseForbidden('No tienes acceso a este prestamo.')

    return render(
        request,
        'biblioteca/detalle_prestamo.html',
        {'prestamo': prestamo},
    )


@login_required
@permission_required('biblioteca.puede_gestionar_biblioteca', raise_exception=True)
def crear_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_libros_biblioteca')
    else:
        form = LibroForm()

    return render(request, 'biblioteca/form_libro.html', {'form': form})


@login_required
@permission_required('biblioteca.puede_gestionar_biblioteca', raise_exception=True)
def actualizar_estado_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    estado_anterior = prestamo.estado

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in {'ACT', 'DEV', 'ATR'}:
            prestamo.estado = nuevo_estado
            prestamo.save(update_fields=['estado'])

            libro = prestamo.libro
            if estado_anterior != 'DEV' and nuevo_estado == 'DEV':
                libro.ejemplares_disponibles += 1
                libro.save(update_fields=['ejemplares_disponibles'])
            elif estado_anterior == 'DEV' and nuevo_estado != 'DEV':
                if libro.ejemplares_disponibles > 0:
                    libro.ejemplares_disponibles -= 1
                    libro.save(update_fields=['ejemplares_disponibles'])

        return redirect('detalle_prestamo_biblioteca', prestamo_id=prestamo.id)

    return render(
        request,
        'biblioteca/actualizar_prestamo.html',
        {'prestamo': prestamo, 'estados': Prestamo.ESTADOS},
    )
