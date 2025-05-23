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
   ```bash
   git clone https://github.com/tu-usuario/cotizaciones-automatica.git
   cd cotizaciones-automatica
   ```

2. **Configura el entorno Python**
   ```bash
   python -m venv .venv
   # Activar el entorno virtual en Linux/Mac
   source .venv/bin/activate

   # Activar el entorno virtual en Windows
   .venv\Scripts\activate

   # Instalar dependencias
   pip install -r requirements.txt
   ```
