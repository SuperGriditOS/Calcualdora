#!/usr/bin/env python3
"""
Interfaz web para la Calculadora de Gastos Compartidos
Desarrollada con Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
from typing import List, Dict, Tuple

# Importar nuestros modelos y servicios
from models.persona import Persona
from models.gasto import Gasto
from models.grupo import Grupo
from services.balance_service import BalanceService
from services.simplificador_service import SimplificadorService


# Configuración de la página
st.set_page_config(
    page_title="🧮 Calculadora de Gastos Compartidos",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .section-header {
        font-size: 1.8rem;
        color: #A23B72;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #F18F01;
        padding-bottom: 0.5rem;
    }
    
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    
    .info-message {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    
    .balance-positive {
        color: #dc3545;
        font-weight: bold;
    }
    
    .balance-negative {
        color: #28a745;
        font-weight: bold;
    }
    
    .balance-zero {
        color: #6c757d;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar servicios
@st.cache_resource
def get_services():
    """Obtiene las instancias de los servicios (con cache)."""
    balance_service = BalanceService()
    simplificador_service = SimplificadorService(balance_service)
    return balance_service, simplificador_service

# Inicializar estado de la sesión
def init_session_state():
    """Inicializa el estado de la sesión si no existe."""
    if 'grupo_actual' not in st.session_state:
        st.session_state.grupo_actual = None
    if 'personas_cache' not in st.session_state:
        st.session_state.personas_cache = {}
    if 'gastos_registrados' not in st.session_state:
        st.session_state.gastos_registrados = []

def main():
    """Función principal de la aplicación web."""
    
    # Inicializar estado
    init_session_state()
    balance_service, simplificador_service = get_services()
    
    # Header principal
    st.markdown('<h1 class="main-header">🧮 Calculadora de Gastos Compartidos</h1>', unsafe_allow_html=True)
    
    # Sidebar para navegación
    with st.sidebar:
        st.markdown("### 🧭 Navegación")
        page = st.selectbox(
            "Selecciona una sección:",
            ["🏠 Inicio", "👥 Gestión de Grupos", "💰 Registrar Gastos", 
             "📊 Ver Balances", "🔄 Simplificar Deudas", "📈 Análisis y Reportes"]
        )
        
        # Información del grupo actual
        if st.session_state.grupo_actual:
            st.markdown("### 📋 Grupo Actual")
            st.info(f"**{st.session_state.grupo_actual.nombre}**\n\n"
                   f"👥 Miembros: {len(st.session_state.grupo_actual.miembros)}\n"
                   f"💸 Gastos: {len(st.session_state.grupo_actual.gastos)}")
        else:
            st.markdown("### ⚠️ Sin Grupo")
            st.warning("No hay un grupo activo. Crea uno para comenzar.")
    
    # Navegación entre páginas
    if page == "🏠 Inicio":
        show_home_page(balance_service, simplificador_service)
    elif page == "👥 Gestión de Grupos":
        show_group_management_page()
    elif page == "💰 Registrar Gastos":
        show_expense_registration_page()
    elif page == "📊 Ver Balances":
        show_balances_page(balance_service)
    elif page == "🔄 Simplificar Deudas":
        show_debt_simplification_page(simplificador_service)
    elif page == "📈 Análisis y Reportes":
        show_analysis_page(balance_service, simplificador_service)

def show_home_page(balance_service, simplificador_service):
    """Muestra la página de inicio."""
    st.markdown('<h2 class="section-header">🏠 Bienvenido a tu Calculadora de Gastos</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 ¿Qué puedes hacer?
        
        - **👥 Crear grupos** de personas que comparten gastos
        - **💰 Registrar gastos** con quién pagó y quién se beneficia
        - **📊 Ver balances** individuales de cada persona
        - **🔄 Simplificar deudas** para minimizar transferencias
        - **📈 Analizar patrones** de gastos con gráficos
        
        ### 🚀 Comienza aquí:
        1. Ve a **Gestión de Grupos** para crear tu primer grupo
        2. Agrega personas al grupo
        3. Registra gastos en **Registrar Gastos**
        4. Ve los resultados en **Ver Balances**
        """)
    
    with col2:
        if st.session_state.grupo_actual:
            # Mostrar resumen rápido del grupo actual
            st.markdown("### 📋 Resumen del Grupo Actual")
            
            balances = balance_service.calcular_balance_grupo(st.session_state.grupo_actual)
            deudores, acreedores = balance_service.obtener_resumen_balances(st.session_state.grupo_actual)
            
            col2_1, col2_2 = st.columns(2)
            with col2_1:
                st.metric("👥 Miembros", len(st.session_state.grupo_actual.miembros))
                st.metric("💸 Gastos", len(st.session_state.grupo_actual.gastos))
            
            with col2_2:
                st.metric("🔴 Deudores", len(deudores))
                st.metric("🟢 Acreedores", len(acreedores))
            
            # Mostrar últimas transferencias necesarias
            if deudores or acreedores:
                st.markdown("#### 🔄 Transferencias Necesarias")
                transferencias = simplificador_service.simplificar_deudas(st.session_state.grupo_actual)
                
                if transferencias:
                    for i, transferencia in enumerate(transferencias[:3], 1):
                        st.write(f"{i}. {transferencia.de.nombre} → {transferencia.para.nombre}: ${transferencia.monto:.2f}")
                    
                    if len(transferencias) > 3:
                        st.write(f"... y {len(transferencias) - 3} más")
                else:
                    st.success("🎉 ¡No hay deudas pendientes!")
        else:
            st.markdown("### 🚀 ¡Comienza Creando un Grupo!")
            st.info("Ve a **Gestión de Grupos** para crear tu primer grupo y comenzar a registrar gastos.")

def show_group_management_page():
    """Muestra la página de gestión de grupos."""
    st.markdown('<h2 class="section-header">👥 Gestión de Grupos</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🏗️ Crear/Editar Grupo", "👤 Gestionar Personas"])
    
    with tab1:
        st.markdown("### 🏗️ Crear o Editar Grupo")
        
        # Crear nuevo grupo
        with st.form("crear_grupo"):
            st.markdown("#### Crear Nuevo Grupo")
            nombre_grupo = st.text_input("Nombre del grupo:", placeholder="Ej: Viaje a la playa, Cena entre amigos...")
            
            col1, col2 = st.columns(2)
            with col1:
                crear_grupo = st.form_submit_button("🏗️ Crear Grupo", type="primary")
            
            if crear_grupo:
                if nombre_grupo.strip():
                    if st.session_state.grupo_actual:
                        st.session_state.grupo_actual = None  # Limpiar grupo anterior
                    
                    st.session_state.grupo_actual = Grupo(nombre_grupo.strip())
                    st.session_state.personas_cache = {}
                    st.session_state.gastos_registrados = []
                    
                    st.success(f"✅ Grupo '{nombre_grupo}' creado exitosamente!")
                    st.rerun()
                else:
                    st.error("❌ Por favor ingresa un nombre para el grupo.")
        
        # Información del grupo actual
        if st.session_state.grupo_actual:
            st.markdown("#### 📋 Información del Grupo Actual")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Nombre", st.session_state.grupo_actual.nombre)
            with col2:
                st.metric("Miembros", len(st.session_state.grupo_actual.miembros))
            with col3:
                st.metric("Gastos", len(st.session_state.grupo_actual.gastos))
            
            # Opción para limpiar grupo
            if st.button("🗑️ Limpiar Grupo Actual"):
                st.session_state.grupo_actual = None
                st.session_state.personas_cache = {}
                st.session_state.gastos_registrados = []
                st.success("✅ Grupo limpiado exitosamente!")
                st.rerun()
    
    with tab2:
        st.markdown("### 👤 Gestionar Personas")
        
        if not st.session_state.grupo_actual:
            st.warning("⚠️ Primero crea un grupo para gestionar personas.")
        else:
            # Agregar persona
            with st.form("agregar_persona"):
                st.markdown("#### ➕ Agregar Persona")
                nombre_persona = st.text_input("Nombre de la persona:", placeholder="Ej: Juan, María, Pedro...")
                
                if st.form_submit_button("➕ Agregar al Grupo"):
                    if nombre_persona.strip():
                        # Verificar si ya existe
                        if nombre_persona.strip() in st.session_state.personas_cache:
                            persona = st.session_state.personas_cache[nombre_persona.strip()]
                        else:
                            persona = Persona(nombre_persona.strip())
                            st.session_state.personas_cache[nombre_persona.strip()] = persona
                        
                        if st.session_state.grupo_actual.agregar_miembro(persona):
                            st.success(f"✅ {persona.nombre} agregado al grupo!")
                            st.rerun()
                        else:
                            st.warning(f"⚠️ {persona.nombre} ya está en el grupo.")
                    else:
                        st.error("❌ Por favor ingresa un nombre válido.")
            
            # Listar personas actuales
            if st.session_state.grupo_actual.miembros:
                st.markdown("#### 👥 Miembros Actuales")
                
                # Crear DataFrame para mostrar en tabla
                personas_data = []
                for i, persona in enumerate(st.session_state.grupo_actual.miembros, 1):
                    personas_data.append({
                        "N°": i,
                        "Nombre": persona.nombre,
                        "ID": persona.id
                    })
                
                df_personas = pd.DataFrame(personas_data)
                st.dataframe(df_personas, use_container_width=True, hide_index=True)
                
                # Opción para remover persona
                if len(st.session_state.grupo_actual.miembros) > 0:
                    st.markdown("#### 🗑️ Remover Persona")
                    
                    with st.form("remover_persona"):
                        persona_a_remover = st.selectbox(
                            "Selecciona una persona para remover:",
                            [p.nombre for p in st.session_state.grupo_actual.miembros]
                        )
                        
                        if st.form_submit_button("🗑️ Remover del Grupo", type="secondary"):
                            # Encontrar la persona
                            persona_obj = next(p for p in st.session_state.grupo_actual.miembros 
                                             if p.nombre == persona_a_remover)
                            
                            if st.session_state.grupo_actual.remover_miembro(persona_obj):
                                st.success(f"✅ {persona_obj.nombre} removido del grupo!")
                                st.rerun()
                            else:
                                st.error("❌ Error al remover la persona.")

def show_expense_registration_page():
    """Muestra la página de registro de gastos."""
    st.markdown('<h2 class="section-header">💰 Registrar Gastos</h2>', unsafe_allow_html=True)
    
    if not st.session_state.grupo_actual:
        st.warning("⚠️ Primero crea un grupo y agrega personas para registrar gastos.")
        return
    
    if len(st.session_state.grupo_actual.miembros) < 2:
        st.warning("⚠️ Se necesitan al menos 2 personas en el grupo para registrar gastos.")
        return
    
    # Formulario para registrar gasto
    with st.form("registrar_gasto"):
        st.markdown("### ➕ Registrar Nuevo Gasto")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Seleccionar pagador
            pagador_nombre = st.selectbox(
                "👤 ¿Quién pagó?",
                [p.nombre for p in st.session_state.grupo_actual.miembros]
            )
            
            # Monto
            monto = st.number_input(
                "💰 Monto pagado:",
                min_value=0.01,
                step=0.01,
                format="%.2f"
            )
            
            # Descripción
            descripcion = st.text_input(
                "📝 Descripción del gasto:",
                placeholder="Ej: Cena, Hotel, Gasolina..."
            )
        
        with col2:
            # Seleccionar beneficiarios
            st.markdown("👥 **¿Quién se beneficia de este gasto?**")
            
            beneficiarios_seleccionados = []
            for persona in st.session_state.grupo_actual.miembros:
                if st.checkbox(f"{persona.nombre}", value=True):
                    beneficiarios_seleccionados.append(persona)
            
            if not beneficiarios_seleccionados:
                st.error("❌ Debes seleccionar al menos un beneficiario.")
        
        # Botón de envío
        if st.form_submit_button("💾 Registrar Gasto", type="primary"):
            if beneficiarios_seleccionados and monto > 0 and descripcion.strip():
                # Crear el gasto
                pagador = next(p for p in st.session_state.grupo_actual.miembros 
                             if p.nombre == pagador_nombre)
                
                gasto = Gasto(
                    pagador=pagador,
                    monto=monto,
                    descripcion=descripcion.strip(),
                    beneficiarios=beneficiarios_seleccionados
                )
                
                if st.session_state.grupo_actual.agregar_gasto(gasto):
                    st.session_state.gastos_registrados.append(gasto)
                    st.success(f"✅ Gasto registrado: {gasto}")
                    st.rerun()
                else:
                    st.error("❌ Error al registrar el gasto.")
            else:
                st.error("❌ Por favor completa todos los campos correctamente.")
    
    # Mostrar gastos registrados
    if st.session_state.grupo_actual.gastos:
        st.markdown("### 📋 Gastos Registrados")
        
        # Crear DataFrame para mostrar gastos
        gastos_data = []
        for i, gasto in enumerate(st.session_state.grupo_actual.gastos, 1):
            gastos_data.append({
                "N°": i,
                "Pagador": gasto.pagador.nombre,
                "Monto": f"${gasto.monto:.2f}",
                "Descripción": gasto.descripcion,
                "Beneficiarios": len(gasto.beneficiarios),
                "Monto por Persona": f"${gasto.monto_por_persona():.2f}",
                "Fecha": gasto.fecha.strftime("%d/%m/%Y %H:%M")
            })
        
        df_gastos = pd.DataFrame(gastos_data)
        st.dataframe(df_gastos, use_container_width=True, hide_index=True)

def show_balances_page(balance_service):
    """Muestra la página de balances."""
    st.markdown('<h2 class="section-header">📊 Balances Individuales</h2>', unsafe_allow_html=True)
    
    if not st.session_state.grupo_actual:
        st.warning("⚠️ No hay un grupo activo para mostrar balances.")
        return
    
    if not st.session_state.grupo_actual.gastos:
        st.info("ℹ️ No hay gastos registrados. Los balances están equilibrados.")
        return
    
    # Calcular balances
    balances = balance_service.calcular_balance_grupo(st.session_state.grupo_actual)
    deudores, acreedores = balance_service.obtener_resumen_balances(st.session_state.grupo_actual)
    
    # Verificar conservación de dinero
    conservacion_ok = balance_service.verificar_balance_cero(st.session_state.grupo_actual)
    
    # Métricas generales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Miembros", len(st.session_state.grupo_actual.miembros))
    with col2:
        st.metric("🔴 Deudores", len(deudores))
    with col3:
        st.metric("🟢 Acreedores", len(acreedores))
    with col4:
        st.metric("💰 Total Gastos", f"${sum(g.monto for g in st.session_state.grupo_actual.gastos):.2f}")
    
    # Estado de conservación
    if conservacion_ok:
        st.success("✅ Los balances suman cero (conservación de dinero verificada).")
    else:
        st.error("❌ Error: Los balances no suman cero. Revisa los gastos registrados.")
    
    # Mostrar balances en tabla
    st.markdown("### 💰 Balances por Persona")
    
    balances_data = []
    for persona, balance in balances.items():
        if balance > 0.01:
            estado = "🔴 Debe"
            color = "balance-positive"
        elif balance < -0.01:
            estado = "🟢 Debe Recibir"
            color = "balance-negative"
        else:
            estado = "⚪ Equilibrado"
            color = "balance-zero"
        
        balances_data.append({
            "Persona": persona.nombre,
            "Balance": f"${balance:.2f}",
            "Estado": estado
        })
    
    df_balances = pd.DataFrame(balances_data)
    st.dataframe(df_balances, use_container_width=True, hide_index=True)
    
    # Gráfico de balances
    if len(balances_data) > 0:
        st.markdown("### 📊 Gráfico de Balances")
        
        fig = px.bar(
            df_balances,
            x="Persona",
            y=[float(b.replace("$", "")) for b in df_balances["Balance"]],
            color=[float(b.replace("$", "")) for b in df_balances["Balance"]],
            color_continuous_scale=["red", "white", "green"],
            title="Balances Individuales",
            labels={"y": "Balance ($)", "x": "Persona"}
        )
        
        fig.update_layout(
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_debt_simplification_page(simplificador_service):
    """Muestra la página de simplificación de deudas."""
    st.markdown('<h2 class="section-header">🔄 Simplificación de Deudas</h2>', unsafe_allow_html=True)
    
    if not st.session_state.grupo_actual:
        st.warning("⚠️ No hay un grupo activo para simplificar deudas.")
        return
    
    if not st.session_state.grupo_actual.gastos:
        st.info("ℹ️ No hay gastos registrados. No hay deudas que simplificar.")
        return
    
    # Obtener transferencias simplificadas
    transferencias = simplificador_service.simplificar_deudas(st.session_state.grupo_actual)
    eficiencia = simplificador_service.calcular_eficiencia_simplificacion(st.session_state.grupo_actual)
    
    # Métricas de eficiencia
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔢 Deudas Originales", eficiencia['deudas_originales'])
    with col2:
        st.metric("💸 Transferencias Necesarias", eficiencia['transferencias_necesarias'])
    with col3:
        st.metric("📉 Reducción", f"{eficiencia['reduccion_porcentaje']:.1f}%")
    with col4:
        st.metric("💰 Total a Transferir", f"${eficiencia['monto_total_transferencias']:.2f}")
    
    # Mostrar transferencias
    if transferencias:
        st.markdown("### 💸 Transferencias Necesarias")
        st.info(f"Para saldar todas las deudas, se necesitan **{len(transferencias)} transferencias** "
                f"(reducción del {eficiencia['reduccion_porcentaje']:.1f}%).")
        
        # Crear DataFrame para transferencias
        transferencias_data = []
        for i, transferencia in enumerate(transferencias, 1):
            transferencias_data.append({
                "N°": i,
                "De": transferencia.de.nombre,
                "Para": transferencia.para.nombre,
                "Monto": f"${transferencia.monto:.2f}",
                "Acción": f"💸 Transferir ${transferencia.monto:.2f}"
            })
        
        df_transferencias = pd.DataFrame(transferencias_data)
        st.dataframe(df_transferencias, use_container_width=True, hide_index=True)
        
        # Botón para marcar como pagadas
        st.markdown("### ✅ Gestión de Pagos")
        st.info("Una vez que se realicen las transferencias, puedes marcarlas como completadas.")
        
        if st.button("✅ Marcar Todas como Pagadas", type="primary"):
            st.success("🎉 ¡Todas las transferencias han sido marcadas como completadas!")
    
    else:
        st.success("🎉 ¡Perfecto! No hay deudas que simplificar. Todos los balances están equilibrados.")
        st.balloons()

def show_analysis_page(balance_service, simplificador_service):
    """Muestra la página de análisis y reportes."""
    st.markdown('<h2 class="section-header">📈 Análisis y Reportes</h2>', unsafe_allow_html=True)
    
    if not st.session_state.grupo_actual:
        st.warning("⚠️ No hay un grupo activo para analizar.")
        return
    
    if not st.session_state.grupo_actual.gastos:
        st.info("ℹ️ No hay gastos registrados para analizar.")
        return
    
    # Análisis de gastos por persona
    st.markdown("### 👤 Gastos por Persona")
    
    gastos_por_persona = {}
    for gasto in st.session_state.grupo_actual.gastos:
        if gasto.pagador.nombre not in gastos_por_persona:
            gastos_por_persona[gasto.pagador.nombre] = 0
        gastos_por_persona[gasto.pagador.nombre] += gasto.monto
    
    if gastos_por_persona:
        df_gastos_persona = pd.DataFrame([
            {"Persona": persona, "Total Gastado": f"${monto:.2f}"}
            for persona, monto in gastos_por_persona.items()
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(df_gastos_persona, use_container_width=True, hide_index=True)
        
        with col2:
            # Gráfico de gastos por persona
            fig = px.pie(
                values=list(gastos_por_persona.values()),
                names=list(gastos_por_persona.keys()),
                title="Distribución de Gastos por Persona"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Análisis temporal de gastos
    st.markdown("### 📅 Análisis Temporal")
    
    gastos_temporales = []
    for gasto in st.session_state.grupo_actual.gastos:
        gastos_temporales.append({
            "Fecha": gasto.fecha.date(),
            "Monto": gasto.monto,
            "Pagador": gasto.pagador.nombre,
            "Descripción": gasto.descripcion
        })
    
    if gastos_temporales:
        df_temporal = pd.DataFrame(gastos_temporales)
        
        # Gráfico de gastos en el tiempo
        fig = px.bar(
            df_temporal,
            x="Fecha",
            y="Monto",
            color="Pagador",
            title="Gastos Registrados por Fecha",
            labels={"Monto": "Monto ($)", "Fecha": "Fecha"}
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Estadísticas temporales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📅 Primer Gasto", df_temporal["Fecha"].min().strftime("%d/%m/%Y"))
        with col2:
            st.metric("📅 Último Gasto", df_temporal["Fecha"].max().strftime("%d/%m/%Y"))
        with col3:
            st.metric("📊 Promedio Diario", f"${df_temporal['Monto'].mean():.2f}")
    
    # Exportar datos
    st.markdown("### 📤 Exportar Datos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Exportar Balances"):
            balances = balance_service.calcular_balance_grupo(st.session_state.grupo_actual)
            balances_data = [
                {"Persona": p.nombre, "Balance": f"${b:.2f}"}
                for p, b in balances.items()
            ]
            
            csv = pd.DataFrame(balances_data).to_csv(index=False)
            st.download_button(
                label="⬇️ Descargar CSV",
                data=csv,
                file_name=f"balances_{st.session_state.grupo_actual.nombre}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("💸 Exportar Transferencias"):
            transferencias = simplificador_service.simplificar_deudas(st.session_state.grupo_actual)
            transferencias_data = [
                {
                    "De": t.de.nombre,
                    "Para": t.para.nombre,
                    "Monto": f"${t.monto:.2f}"
                }
                for t in transferencias
            ]
            
            csv = pd.DataFrame(transferencias_data).to_csv(index=False)
            st.download_button(
                label="⬇️ Descargar CSV",
                data=csv,
                file_name=f"transferencias_{st.session_state.grupo_actual.nombre}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("📋 Exportar Resumen"):
            # Crear resumen completo
            balances = balance_service.calcular_balance_grupo(st.session_state.grupo_actual)
            transferencias = simplificador_service.simplificar_deudas(st.session_state.grupo_actual)
            
            resumen = {
                "grupo": st.session_state.grupo_actual.nombre,
                "fecha_reporte": datetime.now().isoformat(),
                "miembros": [p.nombre for p in st.session_state.grupo_actual.miembros],
                "total_gastos": sum(g.monto for g in st.session_state.grupo_actual.gastos),
                "balances": {p.nombre: b for p, b in balances.items()},
                "transferencias": [
                    {
                        "de": t.de.nombre,
                        "para": t.para.nombre,
                        "monto": t.monto
                    }
                    for t in transferencias
                ]
            }
            
            json_data = json.dumps(resumen, indent=2, ensure_ascii=False)
            st.download_button(
                label="⬇️ Descargar JSON",
                data=json_data,
                file_name=f"resumen_{st.session_state.grupo_actual.nombre}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
