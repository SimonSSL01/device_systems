# Device_systems

API REST construida con FastAPI para la gestión del recurso users dentro del sistema device_systems. Incluye validación de datos con Pydantic v2, parámetros de ruta y consulta, modelos de respuesta y cabeceras HTTP personalizadas.

---

**device_systems API** es una API REST construida con FastAPI que permite gestionar usuarios, dispositivos y prestamos de un sistema. La API soporta operaciones **CRUD** completas:

- Usuarios: Crear, listar, consultar, actualizar y eliminar usuarios.
- Dispositivos: Gestionar equipos tecnologicos (laptops, tablets, proyectores, etc.).
- Prestamos: Registrar y gestionar prestamos de dispositivos a usuarios.

Además, implementa validaciones de datos, manejo de errores con códigos HTTP apropiados, inyección de dependencias para validar cabeceras, y documentación automática generada con Swagger.

---

## Ejecución del servidor y instalación de dependencias

Primero tendras que instalar las dependencias con el siguiente comando:

```bash
pip install -r requirements.txt
```

Luego, ejecutamos el servidor con el siguiente comando:

```bash
uvicorn app.main:app --reload
```

La API quedará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Documentación interactiva (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Cabeceras HTTP personalizadas

Todos los endpoints retornan las siguientes cabeceras personalizadas:

```
X-App-Name: device_systems
X-API-Version: 1.0
```
---

## Códigos de estado HTTP

| Código | Significado | Cuándo se usa |
|--------|-------------|----------------|
| 200 | OK | GET, PUT, PATCH, DELETE exitosos |
| 201 | Created | POST exitoso (usuario creado) |
| 400 | Bad Request | Datos inválidos, correo duplicado, rol no permitido, cabeceras incorrectas |
| 404 | Not Found | Usuario no encontrado |
| 422 | Unprocessable Entity | Error de validación de Pydantic (ej. email mal formado) |

--- 

## Endpoints disponibles

### Recurso: Users (`/users`)

| Metodo | Endpoint | Codigo exito | Descripcion |
|--------|----------|--------------|-------------|
| GET | `/users` | 200 | Lista todos los usuarios |
| GET | `/users/{user_id}` | 200 | Obtiene usuario por ID |
| POST | `/users` | 201 | Crea un nuevo usuario |
| PUT | `/users/{user_id}` | 200 | Actualiza completamente un usuario |
| PATCH | `/users/{user_id}` | 200 | Actualiza parcialmente un usuario |
| DELETE | `/users/{user_id}` | 200 | Elimina un usuario |

### Recurso: Devices (`/devices`)

| Metodo | Endpoint | Codigo exito | Descripcion |
|--------|----------|--------------|-------------|
| GET | `/devices` | 200 | Lista dispositivos (con filtros) |
| GET | `/devices/{device_id}` | 200 | Obtiene dispositivo por ID |
| POST | `/devices` | 201 | Crea un nuevo dispositivo |
| PUT | `/devices/{device_id}` | 200 | Actualiza completamente un dispositivo |
| PATCH | `/devices/{device_id}` | 200 | Actualiza parcialmente un dispositivo |
| DELETE | `/devices/{device_id}` | 200 | Elimina un dispositivo |

**Filtros para GET /devices:**
- `?device_type=laptop` - Filtrar por tipo
- `?is_available=true` - Filtrar por disponibilidad
- `?brand=lenovo` - Filtrar por marca
- `?search=thinkpad` - Buscar por nombre o numero de serie

### Recurso: Loans (`/loans`)

| Metodo | Endpoint | Codigo exito | Descripcion |
|--------|----------|--------------|-------------|
| GET | `/loans` | 200 | Lista prestamos (con filtros) |
| GET | `/loans/{loan_id}` | 200 | Obtiene prestamo por ID |
| GET | `/loans/details` | 200 | Prestamos con datos relacionados (JOIN) |
| GET | `/loans/user/{user_id}` | 200 | Prestamos de un usuario |
| GET | `/loans/device/{device_id}` | 200 | Historial de prestamos de un dispositivo |
| POST | `/loans` | 201 | Crea un nuevo prestamo |
| PATCH | `/loans/{loan_id}/return` | 200 | Devuelve un dispositivo |
| DELETE | `/loans/{loan_id}` | 200 | Elimina un prestamo |

**Filtros para GET /loans:**
- `?status=active` - Filtrar por estado (active, returned, overdue)
- `?user_id=1` - Filtrar por usuario
- `?device_id=1` - Filtrar por dispositivo

**Filtros para GET /loans/details:**
- `?status=active` - Filtrar por estado
- `?user_email=ana@example.com` - Filtrar por email del usuario
- `?device_type=laptop` - Filtrar por tipo de dispositivo

---

## Capturas correspondientes a actividad 10 (alembic)

Capturas de alembic, connfirmación de instalación, revision de versiones y historial de cambios:
- ![Alembic](images/img13.png)
- ![Alembic](images/img14.png)
- ![Alembic](images/img15.png)

- Estructura de la carpeta de alembic:

![Alembic](images/img16.png)

--- 

## Capturas de estructura de tablas de la base de datos:
### Usuarios
![users](images/img17.png)
### Dispositivos
![devices](images/img18.png)
### Prestamos
![loans](images/img19.png)



## Capturas de Swagger UI

### 1. Vista general de Swagger UI (solo usuarios)

Captura que muestra todos los endpoints disponibles en la documentación interactiva

![Swagger UI - Vista general](images/img1.png)

---

### 2. Prueba GET `/users`

Evidencia de la ejecución del endpoint GET /users retornando la lista de usuarios.

![GET /users](images/img2.png)
![GET /users](images/img4.png)

---

### 3. Prueba GET `/users/{user_id}`

Evidencia de la consulta de un usuario específico mediante su ID.

![GET /users/{user_id}](images/img5.png)

---

### 4. Prueba POST `/users`

Evidencia del registro exitoso de un nuevo usuario.

![POST /users](images/img3.png)

---

### 5. Prueba PUT `/users`

Evidencia de la actualización exitosa de los datos de un usuario.

![PUT /users](images/img7.png)


---

### 6. Prueba PATCH `/users`

Evidencia del registro exitoso de un nuevo usuario.

![PATCH /users](images/img9.png)

---

### 7. Prueba DELETE `/users`

Evidencia de la eliminación exitosa de un usuario.

![DELETE /users](images/img10.png)

---

### 8. Prueba DELETE `/users`

Evidencia de como quedo la lista de usuarios despues de las pruebas del PUT, PATCH y DELETE.

![GET /users](images/img12.png)

---

### 9. Vista general de swagger (solo devices y loans)

Evidencia de como quedo la vista general de swagger con los nuevos recursos

![New swagger general](images/img20.png)

---
### 10. Prueba GET `/devices`

Se evidencia de como funciona el endpoint y lista los dispositivos.

![GET /devices](images/getalldevices.png)

---
### 11. Prueba GET `/devices/{device_id}`

Se evidencia de como funciona el endpoint y lista solo el dispositivo con la id que se le dio.

![GET /devices/{device_id}](images/getdeviceid.png)

---
### 12. Prueba DELETE `/device`

Se evidencia como funciona el endpoint cuando se quiere eliminar un dispositivo.

![DELETE /devices](images/deletedevice.png)

---
### 13. Prueba PATCH `/device`

Se evidencia como funciona el endpoint cuando se quiere actualizar solo una información de un dispositivo.

![PATCH /devices](images/patchdevices.png)

---
### 14. Prueba PUT `/device`

Se evidencia como funciona el endpoint cuando se quiere actualizar toda la información de un dispositivo.

![PUT /devices](images/putdevices.png)

---
### 15. Prueba POST `/device`

Se evidencia como funciona el endpoint cuando se quiere agregar un nuevo dispositivo.

![POST /devices](images/postdevices.png)

---

### 16. Validaciones y errores

Se evidencia del manejo de errores con un usuario que no puede tener el rol "SuperUser" con el POST.

![Validaciones y errores](images/img6.png)

Se evidencia que no se puede realizar un solo cambio con el PUT.

![Validaciones y errores](images/img8.png)

Se evidencia que no se puede realizar la eliminación de un usuario que ya no existe con el DELETE.

![Validaciones y errores](images/img11.png)

Se evidencia que no se puede realizar el post de un dispositivo ya que no cuenta con un tipo permitido.

![Validaciones y errores](images/errorpostdevice.png)

---

## Como se uso Depends() para reutilizar la logica?
Se creo una dependencia verify_headers que valida las cabeceras X-App-Name y X-API-Version. Luego se le inyecta en todas las rutas con dependencies. Esto para evitar repetir la misma validación en cada endpoint y centralizando la lógica, , ademas, el proyecto utiliza Depends() de FastAPI para reutilizar lógica común entre múltiples endpoints sin repetir código. Las dependencias están definidas en app/dependencies/user_dependencies.py.

---

## Conclusion
El desarrollo de esta API REST con FastAPI permitió aplicar los fundamentos del desarrollo backend moderno, incluyendo la validación de datos con Pydantic, la separación de responsabilidades mediante una arquitectura por capas (rutas, esquemas y controlador), y la generación automática de documentación interactiva con Swagger UI.

Se implementaron exitosamente los endpoints GET, POST, PUT, PATCH y DELETE para la gestión de usuarios, aplicando parámetros de ruta y consulta, manejo de errores en codigo HTTP, cabeceras personalizadas y modelos de respuesta. Además, se garantizó la integridad de los datos mediante validaciones como formato de email, roles permitidos y prevención de correos duplicados.

---

### Video De Sustentación

*   **Enlace al video 1:** https://youtu.be/u5HaJ4sqxFQ
*   **Enlace al video 2:** https://youtu.be/HdFrOCEhPnc
*   **Enlace al video 3:** https://youtu.be/DT0hcw2f51M
*   **Enlace al video 4:** 