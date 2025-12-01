# Auth-service

Servicio centralizado de autenticación construido con FastAPI que gestiona el registro de usuarios, generación y verificación de tokens JWT, y envío de credenciales temporales vía correo electrónico. Expone endpoints para registro, login, validación de tokens y consulta de estadísticas, pensado para integrarse con otros servicios o frontends que requieran autenticación delegada.

## Tecnologías principales

- **FastAPI** para la construcción de la API asíncrona.
- **Motor (MongoDB)** como cliente asíncrono de base de datos.
- **PyJWT** para la generación y validación de tokens.
- **bcrypt** para el hash seguro de contraseñas.
- **python-dotenv** y **pydantic-settings** para la gestión de configuración.
- **Uvicorn** como servidor ASGI para ejecución en desarrollo/producción.
- **httpx** para posibles integraciones HTTP asíncronas.

## Estructura y servicios clave

- `app/main.py`: inicialización de la aplicación, configuración de CORS y endpoints de salud.
- `app/routes/auth.py`: rutas para registro, login, verificación de token y estadísticas.
- `app/services/`: lógica de negocio (autenticación, tokens y correos electrónicos).
- `app/utils/`: utilidades para logging y manejo seguro de contraseñas.
- `app/database.py`: conexión y configuración de índices en MongoDB.
