# 🧮 Calculadora de Gastos Compartidos

Una aplicación completa en Python para gestionar gastos compartidos entre grupos de personas, con simplificación automática de deudas cruzadas.

## ✨ Características

- **👥 Gestión de grupos**: Crear grupos con múltiples personas
- **💰 Registro de gastos**: Registrar gastos con pagador, monto y beneficiarios
- **📊 Cálculo de balances**: Ver cuánto debe cada persona
- **🔄 Simplificación de deudas**: Minimiza el número de transferencias necesarias
- **🖥️ Interfaz CLI**: Interfaz de línea de comandos intuitiva
- **🌐 Interfaz Web**: Aplicación web moderna con Streamlit
- **🧪 Tests completos**: Suite de tests unitarios con pytest

## 🚀 Instalación

1. **Clonar o descargar el proyecto**
```bash
git clone <url-del-repositorio>
cd calculadora-gastos
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 📖 Uso

### 🌐 Interfaz Web (Recomendada)

La interfaz web es la forma más fácil y visual de usar la aplicación:

```bash
# Opción 1: Script automático
python run_web.py

# Opción 2: Comando directo
streamlit run web_app.py
```

**Características de la interfaz web:**
- 🎨 Diseño moderno y responsivo
- 📊 Gráficos interactivos con Plotly
- 📱 Se adapta a móviles y tablets
- 📈 Análisis visual de gastos y balances
- 💾 Exportación de datos en CSV/JSON
- 🔄 Simplificación visual de deudas

### 🖥️ Interfaz CLI

Para usuarios que prefieren la línea de comandos:

```bash
python cli.py
```

### 💻 Uso Programático

```python
from models.persona import Persona
from models.gasto import Gasto
from models.grupo import Grupo
from services.balance_service import BalanceService
from services.simplificador_service import SimplificadorService

# Crear personas
alice = Persona("Alice")
bob = Persona("Bob")
charlie = Persona("Charlie")

# Crear grupo
grupo = Grupo("Viaje a la playa")
grupo.agregar_miembro(alice)
grupo.agregar_miembro(bob)
grupo.agregar_miembro(charlie)

# Registrar gastos
gasto1 = Gasto(
    pagador=alice,
    monto=90.0,
    descripcion="Hotel por 3 noches",
    beneficiarios=[alice, bob, charlie]
)

gasto2 = Gasto(
    pagador=bob,
    monto=45.0,
    descripcion="Comida",
    beneficiarios=[alice, bob, charlie]
)

grupo.agregar_gasto(gasto1)
grupo.agregar_gasto(gasto2)

# Calcular balances
balance_service = BalanceService()
balances = balance_service.calcular_balance_grupo(grupo)

# Simplificar deudas
simplificador = SimplificadorService(balance_service)
transferencias = simplificador.simplificar_deudas(grupo)

print("Transferencias necesarias:")
for t in transferencias:
    print(f"{t.de.nombre} → {t.para.nombre}: ${t.monto:.2f}")
```

## 🧪 Tests

Ejecutar todos los tests:
```bash
pytest
```

Ejecutar tests con cobertura:
```bash
pytest --cov=models --cov=services
```

Ejecutar tests específicos:
```bash
pytest tests/test_balance.py
pytest tests/test_simplificacion.py
```

## 📁 Estructura del Proyecto

```
calculadora_gastos/
├── models/                 # Modelos de datos
│   ├── __init__.py
│   ├── persona.py         # Clase Persona
│   ├── gasto.py          # Clase Gasto
│   └── grupo.py          # Clase Grupo
├── services/              # Servicios de lógica de negocio
│   ├── __init__.py
│   ├── balance_service.py      # Cálculo de balances
│   └── simplificador_service.py # Simplificación de deudas
├── tests/                 # Tests unitarios
│   ├── __init__.py
│   ├── test_balance.py
│   └── test_simplificacion.py
├── .streamlit/            # Configuración de Streamlit
│   └── config.toml
├── cli.py                # Interfaz de línea de comandos
├── web_app.py            # 🌐 Interfaz web con Streamlit
├── run_web.py            # Script para ejecutar la interfaz web
├── install_web.py        # Instalador de dependencias web
├── demo_web.py           # Demo con datos de ejemplo
├── ejemplo_uso.py        # Ejemplos de uso programático
├── requirements.txt      # Dependencias
├── README.md            # Este archivo
└── README_WEB.md        # Documentación específica de la interfaz web
```

## 🔧 Funcionalidades Principales

### 1. Gestión de Personas y Grupos
- Crear personas con nombres únicos
- Agregar/remover miembros de grupos
- Validación de miembros en gastos

### 2. Registro de Gastos
- Especificar quién pagó, cuánto y para quién
- Distribución automática del costo entre beneficiarios
- Timestamps automáticos

### 3. Cálculo de Balances
- Balance neto individual (debe/recibe)
- Deudas detalladas entre pares de personas
- Verificación de conservación de dinero

### 4. Simplificación de Deudas
- Algoritmo para minimizar transferencias
- Eliminación de deudas circulares
- Métricas de eficiencia

### 5. Interfaz Web Avanzada
- Formularios interactivos
- Gráficos y visualizaciones
- Exportación de datos
- Análisis temporal

## 🎯 Algoritmo de Simplificación

El sistema utiliza un algoritmo que:

1. **Calcula balances netos** de cada persona
2. **Separa deudores y acreedores** 
3. **Realiza transferencias directas** para minimizar transacciones
4. **Elimina deudas circulares** cuando es posible

**Ejemplo:**
- Alice debe $10 a Bob
- Bob debe $10 a Charlie  
- Charlie debe $10 a Alice

**Resultado:** No hay transferencias necesarias (se cancelan entre sí)

## 🌐 Despliegue Web

### Despliegue Local
```bash
python run_web.py
# Accede a: http://localhost:8501
```

### Despliegue en Streamlit Cloud
1. Sube el código a GitHub
2. Conecta en [share.streamlit.io](https://share.streamlit.io)
3. ¡Despliega automáticamente!

### Despliegue en Heroku
```bash
# Crear Procfile
echo "web: streamlit run web_app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Desplegar
git add .
git commit -m "Deploy web app"
git push heroku main
```

## 📊 Ejemplo de Resultado

El sistema calcula correctamente balances y simplifica deudas. Por ejemplo, en el caso del viaje:
- **Alice** debe recibir $265.00 (pagó más de lo que debe)
- **Diana, Charlie, Bob** deben pagar proporcionalmente
- **Solo 3 transferencias** necesarias (75% de reducción vs 12 deudas originales)

## 🎭 Demo y Ejemplos

```bash
# Ejecutar demo con datos de ejemplo
python demo_web.py

# Ver ejemplos de uso programático
python ejemplo_uso.py
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🐛 Reportar Bugs

Si encuentras un bug, por favor crea un issue con:
- Descripción detallada del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Información del sistema (OS, versión de Python, etc.)

## 🔮 Roadmap

### ✅ Completado
- [x] Modelos de datos básicos
- [x] Servicios de cálculo y simplificación
- [x] Interfaz CLI completa
- [x] Tests unitarios
- [x] Interfaz web con Streamlit
- [x] Gráficos interactivos
- [x] Exportación de datos

### 🚧 En Desarrollo
- [ ] Persistencia de datos (base de datos)
- [ ] Autenticación de usuarios
- [ ] Notificaciones por email
- [ ] Aplicación móvil

### 💭 Futuro
- [ ] API REST
- [ ] Integración con servicios de pago
- [ ] Reportes en PDF
- [ ] Chat en tiempo real
- [ ] Historial de cambios

---

¡Disfruta usando la calculadora de gastos compartidos! 🎉

**🌐 Para la mejor experiencia, usa la interfaz web: `python run_web.py`**
