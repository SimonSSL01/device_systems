# Device_systems

API REST construida con FastAPI para la gestión del recurso users dentro del sistema device_systems. Incluye validación de datos con Pydantic v2, parámetros de ruta y consulta, modelos de respuesta y cabeceras HTTP personalizadas.

---

**device_systems API** es una API REST construida con FastAPI que permite gestionar usuarios de un sistema. La API soporta operaciones **CRUD** completas:

- **Crear** usuarios
- **Listar** usuarios (con filtros por rol y estado)
- **Consultar** un usuario por su ID
- **Actualizar completamente** un usuario (PUT)
- **Actualizar parcialmente** un usuario (PATCH)
- **Eliminar** usuarios (DELETE)

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


## Capturas de Swagger UI

### 1. Vista general de Swagger UI

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

### 9. Validaciones y errores

Se evidencia del manejo de errores con un usuario que no puede tener el rol "SuperUser" con el POST.

![Validaciones y errores](images/img6.png)

Se evidencia que no se puede realizar un solo cambio con el PUT.

![Validaciones y errores](images/img8.png)

Se evidencia que no se puede realizar la eliminación de un usuario que ya no existe con el DELETE.

![Validaciones y errores](images/img11.png)
---

## Como se uso Depends() para reutilizar la logica?
Se creo una dependencia verify_headers que valida las cabeceras X-App-Name y X-API-Version. Luego se le inyecta en todas las rutas con dependencies. Esto para evitar repetir la misma validación en cada endpoint y centralizando la lógica.

---

## Conclusion
El desarrollo de esta API REST con FastAPI permitió aplicar los fundamentos del desarrollo backend moderno, incluyendo la validación de datos con Pydantic, la separación de responsabilidades mediante una arquitectura por capas (rutas, esquemas y controlador), y la generación automática de documentación interactiva con Swagger UI.

Se implementaron exitosamente los endpoints GET, POST, PUT, PATCH y DELETE para la gestión de usuarios, aplicando parámetros de ruta y consulta, manejo de errores en codigo HTTP, cabeceras personalizadas y modelos de respuesta. Además, se garantizó la integridad de los datos mediante validaciones como formato de email, roles permitidos y prevención de correos duplicados.

---

### Video De Sustentación

*   **Enlace al video 1:** https://youtu.be/u5HaJ4sqxFQ
*   **Enlace al video 2:** 
