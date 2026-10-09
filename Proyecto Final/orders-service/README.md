# Orders Service

API REST para la gestión de órdenes, desarrollada con Python y FastAPI, siguiendo los principios de la arquitectura hexagonal. El proyecto utiliza PostgreSQL como base de datos, SQLAlchemy para el acceso a datos, Alembic para el control de migraciones y JWT para la autenticación de usuarios.

## Arquitectura del proyecto

![Diagrama_orders_service](Evidencia_proyecto_final/Diagrama_orders_service.png)

### 3. Configurar las variables de entorno

Crea un archivo `.env` en la raíz del proyecto.

```dotenv
DATABASE_URL=postgresql+psycopg://orders_user:orders_password@localhost:5432/orders_db

JWT_SECRET_KEY=KEY_SECRETA
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30


```

Genera una clave JWT aleatoria:

```bash
poetry run python -c "import secrets; print(secrets.token_hex(32))"
```

Copia el resultado en `JWT_SECRET_KEY`.

La contraseña se almacena como hash, no como texto plano.

### Evidencias

#### Inición de sesión

![Evidencia_inicio_de_sesion](Evidencia_proyecto_final/Evidencia_inicio_de_sesion.png)
![Evidencia_inicio_de_sesion_2](Evidencia_proyecto_final/Evidencia_inicio_de_sesion_2.png)

#### Crear orden

![Evidencia_crear_orden](Evidencia_proyecto_final/Evidencia_crear_orden.png)
![Evidencia_crear_orden_2](Evidencia_proyecto_final/Evidencia_crear_orden_2.png)

#### Obtener ordenes

![Evidencia_obtener_ordenes](Evidencia_proyecto_final/Evidencia_obtener_ordenes.png)
![Evidencia_obtener_ordenes_2](Evidencia_proyecto_final/Evidencia_obtener_ordenes_2.png)

#### Cancelar orden

![Evidencia_cancelar_orden](Evidencia_proyecto_final/Evidencia_cancelar_orden.png)

#### Auditoria de dependencias

![Evidencia_auditoria_de_dependencias](Evidencia_proyecto_final/Evidencia_auditoria_de_dependencias.png)

#### Test y cobertura

![Evidencia_test_y_cobertura](Evidencia_proyecto_final/Evidencia_test_y_cobertura.png)
