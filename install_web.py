#!/usr/bin/env python3
"""
Script para instalar las dependencias de la interfaz web.
"""

import subprocess
import sys
import os

def install_package(package):
    """Instala un paquete usando pip."""
    try:
        print(f"📦 Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado correctamente.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar {package}: {e}")
        return False

def main():
    """Función principal."""
    print("🧮 Instalador de Dependencias Web")
    print("=" * 40)
    
    # Paquetes necesarios para la interfaz web
    packages = [
        "streamlit>=1.25.0",
        "pandas>=1.5.0",
        "plotly>=5.15.0"
    ]
    
    print("📋 Paquetes a instalar:")
    for package in packages:
        print(f"   • {package}")
    
    print("\n🚀 Iniciando instalación...")
    
    # Instalar cada paquete
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
        print()  # Línea en blanco
    
    # Resumen
    print("=" * 40)
    if success_count == len(packages):
        print("🎉 ¡Todas las dependencias instaladas correctamente!")
        print("\n🚀 Ahora puedes ejecutar la interfaz web:")
        print("   python run_web.py")
        print("   o")
        print("   streamlit run web_app.py")
    else:
        print(f"⚠️ Se instalaron {success_count}/{len(packages)} paquetes.")
        print("💡 Intenta ejecutar manualmente:")
        print("   pip install streamlit pandas plotly")
    
    print("\n📱 La aplicación estará disponible en: http://localhost:8501")

if __name__ == "__main__":
    main()
