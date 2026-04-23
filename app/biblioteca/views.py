from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from .models import Libro, Prestamo
from academico.models import ExpedienteEstudiante

@login_required
def lista_libros(request):
    # Todos los usuarios autenticados pueden ver el catalogo
    libros = Libro.objects.all()
    return render(request, 'biblioteca/lista_libros.html', {'libros': libros})

@login_required
@permission_required('biblioteca.puede_gestionar_biblioteca', raise_exception=True)
def crear_libro(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        isbn = request.POST.get('isbn')
        existencias = request.POST.get('existencias', 1)
        Libro.objects.create(
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            existencias=existencias,
        )
        return redirect('lista_libros')
    return render(request, 'biblioteca/crear_libro.html')

@login_required
def lista_prestamos(request):
    # Admin ve todos, usuario ve solo los suyos
    if request.user.has_perm('biblioteca.puede_gestionar_biblioteca') or request.user.is_superuser:
        prestamos = Prestamo.objects.all().order_by('-fecha_prestamo')
    else:
        try:
            expediente = ExpedienteEstudiante.objects.get(usuario=request.user)
            prestamos = Prestamo.objects.filter(estudiante=expediente).order_by('-fecha_prestamo')
        except ExpedienteEstudiante.DoesNotExist:
            prestamos = Prestamo.objects.none()
    return render(request, 'biblioteca/lista_prestamos.html', {'prestamos': prestamos})

@login_required
def crear_prestamo(request):
    try:
        expediente = ExpedienteEstudiante.objects.get(usuario=request.user)
    except ExpedienteEstudiante.DoesNotExist:
        return HttpResponseForbidden("No tienes un expediente académico registrado.")
    
    if request.method == 'POST':
        libro_id = request.POST.get('libro')
        libro = get_object_or_404(Libro, id=libro_id)
        if libro.existencias <= 0:
            return render(request, 'biblioteca/crear_prestamo.html', {
                'libros': Libro.objects.filter(existencias__gt=0),
                'error': 'No hay existencias disponibles de este libro.'
            })
        Prestamo.objects.create(
            estudiante=expediente,
            libro=libro,
        )
        libro.existencias -= 1
        libro.save()
        return redirect('lista_prestamos')
    
    libros = Libro.objects.filter(existencias__gt=0)
    return render(request, 'biblioteca/crear_prestamo.html', {'libros': libros})

@login_required
def detalle_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)
    # Solo el propietario o admin
    if not request.user.is_superuser:
        try:
            expediente = ExpedienteEstudiante.objects.get(usuario=request.user)
            if prestamo.estudiante != expediente:
                return HttpResponseForbidden("No tienes permiso para ver este préstamo.")
        except ExpedienteEstudiante.DoesNotExist:
            if not request.user.has_perm('biblioteca.puede_gestionar_biblioteca'):
                return HttpResponseForbidden("No tienes permiso para ver este préstamo.")
    return render(request, 'biblioteca/detalle_prestamo.html', {'prestamo': prestamo})

@login_required
@permission_required('biblioteca.puede_gestionar_biblioteca', raise_exception=True)
def actualizar_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)
    if request.method == 'POST':
        devuelto = request.POST.get('devuelto') == 'on'
        fecha_devolucion = request.POST.get('fecha_devolucion') or None
        # Si se marca como devuelto y antes no lo estaba, aumentar existencias
        if devuelto and not prestamo.devuelto:
            prestamo.libro.existencias += 1
            prestamo.libro.save()
        # Si se desmarca como devuelto y antes si lo estaba, disminuir existencias
        elif not devuelto and prestamo.devuelto:
            prestamo.libro.existencias -= 1
            prestamo.libro.save()
        prestamo.devuelto = devuelto
        prestamo.fecha_devolucion = fecha_devolucion
        prestamo.save()
        return redirect('detalle_prestamo', id=prestamo.id)
    return render(request, 'biblioteca/actualizar_prestamo.html', {'prestamo': prestamo})
