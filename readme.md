# 📦 Proyecto Backend - Gestión de Centros, Sectores, Usuarios y Emparejamientos

## 📋 Descripción del proyecto

Este proyecto backend implementa la gestión de una base de datos relacional con las siguientes funcionalidades principales:

- Gestión de **centros** y sus sectores asociados.
- Administración de **usuarios** con roles, asignados a centros y sectores.
- Registro y seguimiento de **emparejamientos** entre usuarios.
- Definición y asignación de **intereses** a usuarios.
- Control de roles para permisos granulares en la plataforma.

La base de datos está diseñada para cubrir los flujos de trabajo necesarios para:

- Definir la estructura organizativa (centros y sectores).
- Registrar usuarios con sus datos personales, roles y asociaciones.
- Gestionar relaciones entre usuarios (emparejamientos).
- Clasificar usuarios por intereses específicos.

---

## 🗂 Estructura de la base de datos

| Tabla                | Descripción                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------------- |
| `centros`            | Lista de centros con id y nombre.                                                                 |
| `sectores`           | Lista de sectores con id y nombre.                                                                |
| `centros_sectores`   | Relación muchos a muchos entre centros y sectores.                                                |
| `roles`              | Definición de roles con permisos para usuarios.                                                   |
| `usuarios`           | Usuarios con datos personales, email único, rol, centro, sector, y otros campos.                  |
| `emparejamientos`    | Registro de emparejamientos entre usuarios con fechas y estado.                                   |
| `intereses`          | Catálogo de intereses con descripciones multilingües y posible fecha de baja.                     |
| `intereses_usuarios` | Relación muchos a muchos entre intereses y usuarios, con posible descripción adicional.           |

---

## ⚙️ Requisitos y entorno

Para desarrollar y ejecutar este backend, necesitas tener instalado:

- Python 3.8 o superior  
- MySQL o MariaDB (usado a través de SQLAlchemy)  
- Servidor SMTP para notificaciones por correo (configurable vía `.env`)  
- Entorno virtual para Python  

---

## 🛠️ Configuración del entorno de base de datos con XAMPP y MariaDB

Este proyecto utiliza **MariaDB**, que viene incluido con **XAMPP**. XAMPP es una herramienta que facilita el desarrollo local al incluir Apache, PHP y MariaDB.

### 🔽 1. Instalar XAMPP

Descarga XAMPP desde:

👉 [https://www.apachefriends.org/index.html](https://www.apachefriends.org/index.html)

Elige la versión adecuada según tu sistema operativo (Windows, macOS o Linux).

### ⚙️ 2. Iniciar servicios

Abre el **Panel de Control de XAMPP** y arranca los siguientes servicios:

- **Apache** (opcional, solo si lo necesitas para PHP)
- **MySQL** (utilizado como **MariaDB**)

### 🧭 3. Acceder a phpMyAdmin (opcional)

Puedes administrar visualmente la base de datos en:

```text
http://localhost/phpmyadmin


## 🚀 Instalación y puesta en marcha

1. **Crear y activar entorno virtual**

```bash
python3 -m venv venv

source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

2. **Instalar dependencias**

-pip install flask flask-cors python-dotenv flask sqlalchemy lask-bcrypt flask-mail flask-jwt-extended
o instalar requirements.txt:
-pip install -r requirements.txt

3. **Configurar variables de entorno**

crear un archivo .env en la raiz con al menos:

DATABASE_URI=mysql+pymysql://usuario:contraseña@host:puerto/base_de_datos

JWT_SECRET_KEY=tu_clave_secreta_jwt

MAIL_SERVER=smtp.tuservidor.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_correo@dominio.com
MAIL_PASSWORD=tu_contraseña_o_token_de_aplicacion
MAIL_DEFAULT_SENDER=tu_correo@dominio.com

---

4. **Ejecutar la aplicación**

python run.py


## 🔐 Autenticación con JWT (JSON Web Token)

Este proyecto utiliza JWT para gestionar la autenticación de usuarios de forma segura.

### 🔧 Cómo funciona

1. **Login de usuario**:  
   El usuario envía su email y contraseña a la ruta `/login`.

2. **Generación del token**:  
   Si las credenciales son correctas, el backend genera un **JWT** con:
   - `identity`: el ID del usuario.
   - Tiempo de expiración configurable.

3. **Token en cliente**:  
   El token devuelto debe ser almacenado por el cliente (por ejemplo, en localStorage) y enviado en cada petición protegida como encabezado:






