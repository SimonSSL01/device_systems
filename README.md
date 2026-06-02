# Device_systems

API REST construida con FastAPI para la gestión del recurso users dentro del sistema device_systems. Incluye validación de datos con Pydantic v2, parámetros de ruta y consulta, modelos de respuesta y cabeceras HTTP personalizadas.

---

## Ejecución del servidor

```bash
uvicorn app.main:app --reload
```

La API quedará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Documentación interactiva (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---


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

### 5. Validaciones y errores

Se evidencia del manejo de errores con un usuario que no puede tener el rol "SuperUser"

![Validaciones y errores](images/img6.png)

---

## Cabeceras HTTP personalizadas

Todos los endpoints retornan las siguientes cabeceras personalizadas:

```
X-App-Name: device_systems
X-API-Version: 1.0
```
---

## Conclusion
El desarrollo de esta API REST con FastAPI permitió aplicar los fundamentos del desarrollo backend moderno, incluyendo la validación de datos con Pydantic, la separación de responsabilidades mediante una arquitectura por capas (rutas, esquemas y controlador), y la generación automática de documentación interactiva con Swagger UI.

Se implementaron exitosamente los endpoints GET y POST para la gestión de usuarios, aplicando parámetros de ruta y consulta, manejo de errores HTTP, cabeceras personalizadas y modelos de respuesta. Además, se garantizó la integridad de los datos mediante validaciones como formato de email, roles permitidos y prevención de correos duplicados.

---

### Video De Sustentación

*   **Enlace al video 1:** https://youtu.be/u5HaJ4sqxFQ
*   **Enlace al video 2:** 

