# Sistema de Cotizaciones Automáticas

Este proyecto implementa un servicio para generar cotizaciones en PDF y enviarlas por correo cuando un cliente completa un formulario. Utiliza:

- **Backend**: Django 4.2 + Django REST Framework  
- **Base de datos**: MySQL  
- **Generación de PDFs**: ReportLab  
- **Filtrado y búsqueda**: django-filter + DRF Search & Ordering  
- **Frontend**: React + Vite  
- **Envío de correo**: SMTP (Gmail u otro proveedor)

---

## 🚀 Características

- CRUD completo de cotizaciones (list, retrieve, create, update, delete)  
- Filtrado por `email`, `nombre`, rango de fechas (`start_date`, `end_date`)  
- Búsqueda en el campo `detalles`  
- Ordenamiento por `fecha` y `precio`  
- Generación automática de PDF al crear/actualizar cotización  
- Envío de PDF adjunto por correo al cliente  

---

## 📦 Requisitos

- Python 3.10+  
- Node.js 16+ / npm o Yarn  
- MySQL 5.7+  
- Git  

---

## 🔧 Instalación

1. **Clona el repositorio**
   ```
   git clone https://github.com/tu-usuario/cotizaciones-automatica.git
   ```
   # Cambia al directorio del repositorio

   ```
   cd cotizaciones-automatica
   ```

2. **Configura el entorno Python**
   # Creacion de entorno Virtual

   ```
   python -m venv .venv
   ```
   # Activar el entorno virtual en Linux/Mac

   ```
   source .venv/bin/activate
   ```

   # Activar el entorno virtual en Windows
   ```
   .venv\Scripts\activate
   ```

   # Instalar dependencias
   ```
   pip install -r requirements.txt
   ```

## ▶️ Uso

1. # Aplica migraciones y crea superusuario

   ```
   python manage.py migrate
   ```
2. # Realiza la creacion de un Superusuario

   ```
   python manage.py createsuperuser
   ```

3. # Inicia el servidor Django

   ```
   python manage.py runserver
   ```

## 📘 API REST

- **Base URL: http://localhost:8000/api/cotizaciones/**

#### Método	Ruta	Descripción
- **GET	/	Lista cotizaciones (con filtros/search/ordering).**
- **POST	/	Crea cotización → genera PDF + envía mail.**
- **GET	/:id/	Recupera cotización por ID.**
- **PUT	/:id/	Actualiza cotización → regenera PDF + reenvía mail.**
- **DELETE	/:id/	Elimina cotización.**

#### Filtros & Búsqueda & Ordenación

- **Filtrar: ?email=juan@ejemplo.com&nombre=María**

- **Rango fechas: ?start_date=2025-01-01&end_date=2025-12-31**

- **Search: ?search=landing**

- **Orden: ?ordering=precio o ?ordering=-fecha**


## 🤝 Contribuciones

## ¡Las contribuciones son bienvenidas!

**Haz un fork del repositorio.** 

**Crea tu rama (git checkout -b feature/nueva-funcionalidad).**

**Commit de tus cambios (git commit -m 'Agrega nueva funcionalidad').**

**Push a la rama (git push origin feature/nueva-funcionalidad).**

**Abre un Pull Request.**