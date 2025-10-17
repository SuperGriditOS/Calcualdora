# 🌐 Interfaz Web - Calculadora de Gastos Compartidos

Una interfaz web moderna y atractiva desarrollada con **Streamlit** para la calculadora de gastos compartidos.

## ✨ Características de la Interfaz Web

### 🎨 Diseño Moderno
- **Interfaz intuitiva** con navegación por pestañas
- **Tema personalizado** con colores atractivos
- **Responsive design** que se adapta a diferentes pantallas
- **Gráficos interactivos** con Plotly

### 📱 Funcionalidades Web

#### 🏠 **Página de Inicio**
- Resumen rápido del grupo actual
- Métricas clave (miembros, gastos, deudores, acreedores)
- Vista previa de transferencias necesarias

#### 👥 **Gestión de Grupos**
- Crear nuevos grupos con nombres personalizados
- Agregar y remover personas del grupo
- Tabla interactiva con todos los miembros
- Validaciones en tiempo real

#### 💰 **Registro de Gastos**
- Formulario intuitivo para registrar gastos
- Selección múltiple de beneficiarios
- Validación automática de datos
- Vista de todos los gastos registrados en tabla

#### 📊 **Balances Individuales**
- Tabla detallada de balances por persona
- Gráfico de barras interactivo
- Métricas de conservación de dinero
- Códigos de color para deudores/acreedores

#### 🔄 **Simplificación de Deudas**
- Algoritmo optimizado para minimizar transferencias
- Métricas de eficiencia (reducción de transacciones)
- Gráfico de red para visualizar transferencias
- Botón para marcar pagos como completados

#### 📈 **Análisis y Reportes**
- Gráficos de distribución de gastos por persona
- Análisis temporal de gastos
- Exportación de datos en CSV y JSON
- Estadísticas avanzadas

## 🚀 Cómo Ejecutar la Interfaz Web

### Opción 1: Script Automático (Recomendado)
```bash
python run_web.py
```

### Opción 2: Comando Directo
```bash
streamlit run web_app.py
```

### Opción 3: Con Puerto Personalizado
```bash
streamlit run web_app.py --server.port 8080
```

## 📦 Instalación de Dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# O instalar solo las dependencias web
pip install streamlit pandas plotly
```

## 🌐 Acceso a la Aplicación

Una vez ejecutada, la aplicación estará disponible en:
- **URL Local**: http://localhost:8501
- **URL Red Local**: http://[tu-ip]:8501

## 🎯 Guía de Uso

### 1. **Crear un Grupo**
- Ve a "👥 Gestión de Grupos"
- Haz clic en "🏗️ Crear Grupo"
- Ingresa el nombre del grupo
- Haz clic en "Crear Grupo"

### 2. **Agregar Personas**
- En la pestaña "👤 Gestionar Personas"
- Ingresa el nombre de cada persona
- Haz clic en "Agregar al Grupo"

### 3. **Registrar Gastos**
- Ve a "💰 Registrar Gastos"
- Completa el formulario:
  - Quién pagó
  - Monto
  - Descripción
  - Quiénes se benefician
- Haz clic en "Registrar Gasto"

### 4. **Ver Resultados**
- **Balances**: Ve cuánto debe cada persona
- **Simplificación**: Ve las transferencias necesarias
- **Análisis**: Explora gráficos y estadísticas

## 🎨 Personalización

### Cambiar Colores del Tema
Edita el archivo `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#2E86AB"      # Color principal
backgroundColor = "#FFFFFF"   # Fondo principal
secondaryBackgroundColor = "#F0F2F6"  # Fondo secundario
textColor = "#262730"        # Color del texto
```

### Modificar Estilos CSS
Edita la sección `<style>` en `web_app.py` para personalizar:
- Colores de las tarjetas
- Tipografías
- Espaciados
- Animaciones

## 📊 Características Técnicas

### 🏗️ Arquitectura
- **Frontend**: Streamlit con componentes nativos
- **Backend**: Servicios Python existentes
- **Gráficos**: Plotly para visualizaciones interactivas
- **Estado**: Streamlit Session State para persistencia

### 📱 Responsive Design
- Se adapta automáticamente a móviles y tablets
- Navegación optimizada para pantallas pequeñas
- Gráficos responsivos

### 🔒 Seguridad
- Validación de entrada en todos los formularios
- Sanitización de datos
- Manejo seguro de errores

## 🚀 Despliegue en Producción

### Heroku
```bash
# Crear Procfile
echo "web: streamlit run web_app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Desplegar
git add .
git commit -m "Deploy web app"
git push heroku main
```

### Streamlit Cloud
1. Sube el código a GitHub
2. Conecta tu repositorio en [share.streamlit.io](https://share.streamlit.io)
3. Configura el archivo de requisitos
4. ¡Despliega!

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "Port already in use"
```bash
streamlit run web_app.py --server.port 8502
```

### Error: "Permission denied"
```bash
chmod +x run_web.py
python run_web.py
```

### La aplicación no se abre en el navegador
- Abre manualmente: http://localhost:8501
- Verifica que el puerto no esté bloqueado por firewall

## 🔮 Próximas Mejoras

- [ ] **Autenticación de usuarios** con login/logout
- [ ] **Persistencia de datos** con base de datos
- [ ] **Notificaciones push** para recordatorios
- [ ] **Modo oscuro** para mejor experiencia nocturna
- [ ] **API REST** para integración con otras apps
- [ ] **Exportación a PDF** de reportes
- [ ] **Chat en tiempo real** entre miembros del grupo
- [ ] **Historial de cambios** con versionado

## 💡 Consejos de Uso

1. **Usa nombres descriptivos** para grupos y gastos
2. **Registra gastos inmediatamente** después de realizarlos
3. **Revisa los balances** regularmente
4. **Exporta datos importantes** como respaldo
5. **Usa la simplificación** para pagos eficientes

## 🤝 Contribuir

¿Tienes ideas para mejorar la interfaz web? ¡Contribuye!

1. Fork el proyecto
2. Crea una rama para tu feature
3. Implementa las mejoras
4. Crea un Pull Request

---

¡Disfruta usando la calculadora de gastos compartidos con interfaz web! 🎉
