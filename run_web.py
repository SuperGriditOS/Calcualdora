#!/usr/bin/env python3
"""
Script para ejecutar la aplicación web de la calculadora de gastos compartidos.
"""

import subprocess
import sys
import os

def check_dependencies():
    """Verifica que las dependencias estén instaladas."""
    try:
        import streamlit
        import pandas
        import plotly
        print("✅ Todas las dependencias están instaladas.")
        return True
    except ImportError as e:
        print(f"❌ Faltan dependencias: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False

def run_web_app():
    """Ejecuta la aplicación web."""
    if not check_dependencies():
        return False
    
    print("🚀 Iniciando la aplicación web...")
    print("📱 La aplicación se abrirá en tu navegador.")
    print("🛑 Presiona Ctrl+C para detener la aplicación.")
    print("-" * 50)
    
    try:
        # Ejecutar streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "web_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario.")
    except Exception as e:
        print(f"❌ Error al ejecutar la aplicación: {e}")
        return False
    
    return True

def main():
    """Función principal."""
    print("🧮 Calculadora de Gastos Compartidos - Interfaz Web")
    print("=" * 60)
    
    # Verificar que el archivo web_app.py existe
    if not os.path.exists("web_app.py"):
        print("❌ No se encontró el archivo web_app.py")
        print("💡 Asegúrate de estar en el directorio correcto del proyecto.")
        return
    
    # Ejecutar la aplicación
    if run_web_app():
        print("✅ Aplicación ejecutada exitosamente.")
    else:
        print("❌ Error al ejecutar la aplicación.")

if __name__ == "__main__":
    main()
