# IntranetProject

**Materia:** Internet II, Ciclo I 2026
proyecto de la creacion de una intranet en una universidad para la materia de INTERNET II.

## Integrantes (Usuarios del Sistema)

| Nombre                  | Carnet       | Perfil / Nivel de Acceso            |
|:----------------------- |:------------ |:----------------------------------- |
| Gerson Steven Chachagua | 17-0954-2023 | **Administrador** (Acceso Total)    |
| Guillermo Steven Chávez | 17-2350-2023 | **Modificación** (Edición de datos) |
| Rodrigo José Rivera     | 17-2097-2023 | **Modificación** (Edición de datos) |
| Carlos Emanuel Medina   | 17-1916-2020 | **Consulta** (Solo lectura)         |

## Stack de tecnologias

- **Lenguaje:** Python 3.12+
- **Framework:** Django 6.0.4
- **Base de Datos:** SQLite
- **Frontend:** HTML5, CSS3, Bootstrap 5

## Modulos Implementados

1. **Modulo Academico:** Gestión de notas y expedientes (Funcional).
2. **Recursos Humanos:** Control de personal docente y administrativo.
3. **Finanzas:** Pagos y aranceles universitarios.
4. **Soporte IT:** Gestión de tickets y activos tecnológicos.
5. **Registro:** Inscripción de materias y ciclos.
6. **Biblioteca:** Inventario de libros y préstamos.

## Instalación y Ejecución (Local)

1. **Clonar el repositorio:**
   git clone https://github.com/Chasty23/IntranetProject.git
   cd IntranetProject

2. Crear y activar entorno virtual
    python3 -m venv env
    source env/bin/activate  #Linux
    python -m venv nombre_del_entorno #windows  

3. Instalar dependencias
    pip install -r requirements.txt

4. aplicar las migraciones y correr el servidor
    python manage.py migrate
    python manage.py runserver

# Documentacion de endpoints

| **Recurso**          | **Método**   | **URL**          | **Descripción**                                                    |
| -------------------- | ------------ | ---------------- | ------------------------------------------------------------------ |
| **Página de Inicio** | `GET`        | `/`              | Panel principal con acceso a los 6 módulos (Home). Requiere login. |
| **Inicio de Sesión** | `GET / POST` | `/admin/login/`  | Autenticación de usuarios mediante el sistema de staff de Django.  |
| **Cierre de Sesión** | `GET`        | `/admin/logout/` | Finaliza la sesión actual del usuario de forma segura.             |



## modulo academico

| **Recurso**          | **Método**   | **URL**                             | **Nivel de Acceso / Permiso**                                    |
| -------------------- | ------------ | ----------------------------------- | ---------------------------------------------------------------- |
| **Listado de Notas** | `GET`        | `/academico/notas/`                 | **Consulta**: Todos los miembros del grupo.                      |
| **Actualizar Notas** | `GET / POST` | `/academico/notas/editar/<int:id>/` | **Modificación**: Guillermo y Rodrigo (`academico.change_nota`). |

## modulo recursos humanos

| **Recurso**             | **Método**   | **URL**                            | **Nivel de Acceso / Permiso**                                    |
| ----------------------- | ------------ | ---------------------------------- | ---------------------------------------------------------------- |
| **Listado de Personal** | `GET`        | `/rrhh/personal/`                  | **Consulta**: Todos los miembros del grupo.                      |
| **Gestión de Empleado** | `GET / POST` | `/rrhh/personal/detalle/<int:id>/` | **Modificación**: Solo usuarios con `rrhh.puede_gestionar_rrhh`. |



## modulo de finanzas

| **Recurso**          | **Método** | **URL**                    | **Nivel de Acceso / Permiso**                                       |
| -------------------- | ---------- | -------------------------- | ------------------------------------------------------------------- |
| **Estado de Cuenta** | `GET`      | `/finanzas/estado-cuenta/` | **Privado**: Alumnos (Steven/Carlos) solo ven sus propios pagos.    |
| **Auditoría Global** | `GET`      | `/finanzas/estado-cuenta/` | **Admin**: Guillermo/Gerson ven el listado total de la institución. |
## modulo soporte it

Este modulo permite registrar y dar seguimiento a tickets de soporte tecnico dentro de la intranet.

- Los usuarios comunes pueden crear tickets y ver los propios.
- El personal de IT puede atender los tickets asignados.
- El administrador puede ver y gestionar todos los tickets.

| **Recurso**            | **Metodo**   | **URL**                                   | **Nivel de Acceso / Permiso**                       |
| ---------------------- | ------------ | ----------------------------------------- | --------------------------------------------------- |
| **Listado de Tickets** | `GET`        | `/soporte-it/tickets/`                    | **Consulta**: Segun rol del usuario autenticado.    |
| **Crear Ticket**       | `GET / POST` | `/soporte-it/tickets/crear/`              | **Usuario comun**: Puede registrar nuevos tickets.  |
| **Detalle de Ticket**  | `GET`        | `/soporte-it/tickets/<int:id>/`           | **Privado**: Solicitante, tecnico asignado o admin. |
| **Editar Ticket**      | `GET / POST` | `/soporte-it/tickets/<int:id>/editar/`    | **Privado**: Solicitante o admin.                   |
| **Gestionar Ticket**   | `GET / POST` | `/soporte-it/tickets/<int:id>/gestionar/` | **IT / Admin**: Cambio de estado y asignacion.      |
| **Eliminar Ticket**    | `GET / POST` | `/soporte-it/tickets/<int:id>/eliminar/`  | **Privado**: Solicitante o admin.                   |

## modulo registro

Este modulo se integra con el modulo academico para permitir la inscripcion de materias por ciclo academico sin modificar las entidades existentes.

- Reutiliza `ExpedienteEstudiante` y `Materia` del modulo academico.
- Permite registrar ciclos academicos.
- Permite inscribir materias por alumno y por ciclo.

| **Recurso**                  | **Metodo**   | **URL**                                      | **Nivel de Acceso / Permiso**                                       |
| ---------------------------- | ------------ | -------------------------------------------- | ------------------------------------------------------------------- |
| **Listado de Inscripciones** | `GET`        | `/registro/inscripciones/`                   | **Consulta**: Usuario ve las propias; admin ve todas.               |
| **Nueva Inscripcion**        | `GET / POST` | `/registro/inscripciones/crear/`             | **Usuario comun**: Si tiene expediente academico.                   |
| **Detalle de Inscripcion**   | `GET`        | `/registro/inscripciones/<int:id>/`          | **Privado**: Alumno propietario o admin.                            |
| **Eliminar Inscripcion**     | `GET / POST` | `/registro/inscripciones/<int:id>/eliminar/` | **Privado**: Alumno propietario o admin.                            |
| **Listado de Ciclos**        | `GET`        | `/registro/ciclos/`                          | **Gestion**: Solo usuarios con `registro.puede_gestionar_registro`. |
| **Crear Ciclo**              | `GET / POST` | `/registro/ciclos/crear/`                    | **Gestion**: Solo usuarios con `registro.puede_gestionar_registro`. |

## modulo biblioteca

Este modulo administra el inventario de libros y el control de prestamos a estudiantes registrados en la intranet.

- Reutiliza `ExpedienteEstudiante` del modulo academico.
- Controla existencias disponibles por libro.
- Permite registrar prestamos y devoluciones.

| **Recurso**              | **Metodo**   | **URL**                                      | **Nivel de Acceso / Permiso**                                          |
| ------------------------ | ------------ | -------------------------------------------- | ---------------------------------------------------------------------- |
| **Listado de Libros**    | `GET`        | `/biblioteca/libros/`                        | **Consulta**: Todos los usuarios autenticados.                         |
| **Crear Libro**          | `GET / POST` | `/biblioteca/libros/crear/`                  | **Gestion**: Solo usuarios con `biblioteca.puede_gestionar_biblioteca`. |
| **Listado de Prestamos** | `GET`        | `/biblioteca/prestamos/`                     | **Consulta**: Usuario ve los propios; admin ve todos.                  |
| **Nuevo Prestamo**       | `GET / POST` | `/biblioteca/prestamos/crear/`               | **Usuario comun**: Si tiene expediente academico.                      |
| **Detalle de Prestamo**  | `GET`        | `/biblioteca/prestamos/<int:id>/`            | **Privado**: Usuario propietario o admin.                              |
| **Actualizar Prestamo**  | `GET / POST` | `/biblioteca/prestamos/<int:id>/actualizar/` | **Gestion**: Solo usuarios con `biblioteca.puede_gestionar_biblioteca`. |
