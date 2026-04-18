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