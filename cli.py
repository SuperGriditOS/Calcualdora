#!/usr/bin/env python3
"""
Interfaz de línea de comandos para la calculadora de gastos compartidos.
"""

import sys
from typing import List, Optional
from models.persona import Persona
from models.gasto import Gasto
from models.grupo import Grupo
from services.balance_service import BalanceService
from services.simplificador_service import SimplificadorService


class CalculadoraCLI:
    """
    Interfaz de línea de comandos para la calculadora de gastos.
    """
    
    def __init__(self):
        self.grupo_actual: Optional[Grupo] = None
        self.balance_service = BalanceService()
        self.simplificador_service = SimplificadorService(self.balance_service)
        self.personas_registradas = {}  # Cache de personas por nombre
    
    def ejecutar(self):
        """Punto de entrada principal de la aplicación CLI."""
        print("🧮 Calculadora de Gastos Compartidos")
        print("=" * 40)
        
        while True:
            try:
                self.mostrar_menu()
                opcion = input("\nSelecciona una opción: ").strip()
                
                if opcion == "1":
                    self.crear_grupo()
                elif opcion == "2":
                    self.agregar_persona()
                elif opcion == "3":
                    self.registrar_gasto()
                elif opcion == "4":
                    self.mostrar_balances()
                elif opcion == "5":
                    self.mostrar_simplificacion()
                elif opcion == "6":
                    self.mostrar_resumen_grupo()
                elif opcion == "7":
                    self.listar_gastos()
                elif opcion == "0":
                    print("¡Hasta luego! 👋")
                    break
                else:
                    print("❌ Opción no válida. Intenta de nuevo.")
                    
            except KeyboardInterrupt:
                print("\n\n¡Hasta luego! 👋")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def mostrar_menu(self):
        """Muestra el menú principal."""
        print("\n📋 MENÚ PRINCIPAL")
        print("-" * 20)
        print("1. Crear nuevo grupo")
        print("2. Agregar persona al grupo")
        print("3. Registrar gasto")
        print("4. Ver balances individuales")
        print("5. Ver simplificación de deudas")
        print("6. Resumen del grupo")
        print("7. Listar todos los gastos")
        print("0. Salir")
    
    def crear_grupo(self):
        """Crea un nuevo grupo."""
        if self.grupo_actual is not None:
            confirmar = input("¿Deseas crear un nuevo grupo? Esto eliminará el grupo actual. (s/N): ")
            if confirmar.lower() != 's':
                return
        
        nombre = input("Nombre del grupo: ").strip()
        if not nombre:
            print("❌ El nombre del grupo no puede estar vacío.")
            return
        
        self.grupo_actual = Grupo(nombre)
        print(f"✅ Grupo '{nombre}' creado exitosamente.")
    
    def agregar_persona(self):
        """Agrega una persona al grupo actual."""
        if not self._verificar_grupo():
            return
        
        nombre = input("Nombre de la persona: ").strip()
        if not nombre:
            print("❌ El nombre no puede estar vacío.")
            return
        
        # Verificar si la persona ya existe en el cache
        if nombre in self.personas_registradas:
            persona = self.personas_registradas[nombre]
        else:
            persona = Persona(nombre)
            self.personas_registradas[nombre] = persona
        
        if self.grupo_actual.agregar_miembro(persona):
            print(f"✅ {persona.nombre} agregado al grupo.")
        else:
            print(f"⚠️ {persona.nombre} ya está en el grupo.")
    
    def registrar_gasto(self):
        """Registra un nuevo gasto en el grupo."""
        if not self._verificar_grupo():
            return
        
        if len(self.grupo_actual.miembros) < 2:
            print("❌ Se necesitan al menos 2 personas en el grupo para registrar gastos.")
            return
        
        # Obtener pagador
        print("\n👤 Selecciona quién pagó:")
        pagador = self._seleccionar_persona()
        if not pagador:
            return
        
        # Obtener monto
        try:
            monto = float(input("💰 Monto pagado: $"))
            if monto <= 0:
                print("❌ El monto debe ser mayor a 0.")
                return
        except ValueError:
            print("❌ Monto inválido.")
            return
        
        # Obtener descripción
        descripcion = input("📝 Descripción del gasto: ").strip()
        if not descripcion:
            descripcion = "Gasto sin descripción"
        
        # Obtener beneficiarios
        print("\n👥 Selecciona los beneficiarios (personas que se benefician del gasto):")
        beneficiarios = []
        
        while True:
            print(f"Beneficiarios actuales: {[b.nombre for b in beneficiarios]}")
            beneficiario = self._seleccionar_persona("Selecciona un beneficiario (o Enter para terminar): ")
            
            if not beneficiario:
                break
            
            if beneficiario not in beneficiarios:
                beneficiarios.append(beneficiario)
                print(f"✅ {beneficiario.nombre} agregado como beneficiario.")
            else:
                print(f"⚠️ {beneficiario.nombre} ya es beneficiario.")
        
        if not beneficiarios:
            print("❌ Se debe seleccionar al menos un beneficiario.")
            return
        
        # Crear y agregar el gasto
        gasto = Gasto(pagador=pagador, monto=monto, descripcion=descripcion, beneficiarios=beneficiarios)
        
        if self.grupo_actual.agregar_gasto(gasto):
            print(f"✅ Gasto registrado: {gasto}")
        else:
            print("❌ Error al registrar el gasto.")
    
    def mostrar_balances(self):
        """Muestra los balances individuales del grupo."""
        if not self._verificar_grupo():
            return
        
        balances = self.balance_service.calcular_balance_grupo(self.grupo_actual)
        
        print(f"\n💰 BALANCES DEL GRUPO '{self.grupo_actual.nombre}'")
        print("=" * 50)
        
        for persona, balance in balances.items():
            if balance > 0.01:
                print(f"🔴 {persona.nombre}: Debe ${balance:.2f}")
            elif balance < -0.01:
                print(f"🟢 {persona.nombre}: Debe recibir ${abs(balance):.2f}")
            else:
                print(f"⚪ {persona.nombre}: Balance equilibrado")
        
        # Verificar conservación de dinero
        if self.balance_service.verificar_balance_cero(self.grupo_actual):
            print("\n✅ Los balances suman cero (conservación de dinero verificada).")
        else:
            print("\n⚠️ Advertencia: Los balances no suman cero.")
    
    def mostrar_simplificacion(self):
        """Muestra la simplificación de deudas."""
        if not self._verificar_grupo():
            return
        
        transferencias = self.simplificador_service.simplificar_deudas(self.grupo_actual)
        eficiencia = self.simplificador_service.calcular_eficiencia_simplificacion(self.grupo_actual)
        
        print(f"\n🔄 SIMPLIFICACIÓN DE DEUDAS - GRUPO '{self.grupo_actual.nombre}'")
        print("=" * 60)
        
        if not transferencias:
            print("🎉 ¡No hay deudas que simplificar! Todos los balances están equilibrados.")
            return
        
        print("💸 Transferencias necesarias para saldar todas las deudas:")
        print("-" * 50)
        
        for i, transferencia in enumerate(transferencias, 1):
            print(f"{i}. {transferencia}")
        
        print(f"\n📊 ESTADÍSTICAS DE SIMPLIFICACIÓN:")
        print(f"   • Deudas originales: {eficiencia['deudas_originales']}")
        print(f"   • Transferencias necesarias: {eficiencia['transferencias_necesarias']}")
        print(f"   • Reducción: {eficiencia['reduccion_porcentaje']:.1f}%")
        print(f"   • Monto total a transferir: ${eficiencia['monto_total_transferencias']:.2f}")
    
    def mostrar_resumen_grupo(self):
        """Muestra un resumen completo del grupo."""
        if not self._verificar_grupo():
            return
        
        print(f"\n📋 RESUMEN DEL GRUPO '{self.grupo_actual.nombre}'")
        print("=" * 50)
        print(f"👥 Miembros: {len(self.grupo_actual.miembros)}")
        for miembro in self.grupo_actual.miembros:
            print(f"   • {miembro.nombre}")
        
        print(f"\n💸 Gastos registrados: {len(self.grupo_actual.gastos)}")
        
        deudores, acreedores = self.balance_service.obtener_resumen_balances(self.grupo_actual)
        
        if deudores:
            print(f"\n🔴 DEUDORES:")
            for persona, monto in deudores:
                print(f"   • {persona.nombre}: ${monto:.2f}")
        
        if acreedores:
            print(f"\n🟢 ACREEDORES:")
            for persona, monto in acreedores:
                print(f"   • {persona.nombre}: ${monto:.2f}")
    
    def listar_gastos(self):
        """Lista todos los gastos del grupo."""
        if not self._verificar_grupo():
            return
        
        if not self.grupo_actual.gastos:
            print("📝 No hay gastos registrados en el grupo.")
            return
        
        print(f"\n📝 GASTOS DEL GRUPO '{self.grupo_actual.nombre}'")
        print("=" * 50)
        
        for i, gasto in enumerate(self.grupo_actual.gastos, 1):
            print(f"{i}. {gasto}")
            print(f"   Beneficiarios: {', '.join([b.nombre for b in gasto.beneficiarios])}")
            print(f"   Monto por persona: ${gasto.monto_por_persona():.2f}")
            print(f"   Fecha: {gasto.fecha.strftime('%Y-%m-%d %H:%M')}")
            print()
    
    def _verificar_grupo(self) -> bool:
        """Verifica si existe un grupo actual."""
        if self.grupo_actual is None:
            print("❌ No hay un grupo activo. Crea un grupo primero.")
            return False
        return True
    
    def _seleccionar_persona(self, mensaje: str = None) -> Optional[Persona]:
        """Permite al usuario seleccionar una persona del grupo."""
        if not self.grupo_actual.miembros:
            print("❌ No hay miembros en el grupo.")
            return None
        
        if mensaje is None:
            mensaje = "Selecciona una persona:"
        
        print(f"\n{mensaje}")
        for i, persona in enumerate(self.grupo_actual.miembros, 1):
            print(f"{i}. {persona.nombre}")
        
        try:
            opcion = int(input("Número: ")) - 1
            if 0 <= opcion < len(self.grupo_actual.miembros):
                return self.grupo_actual.miembros[opcion]
            else:
                print("❌ Opción inválida.")
                return None
        except ValueError:
            print("❌ Ingresa un número válido.")
            return None


def main():
    """Función principal para ejecutar la aplicación."""
    try:
        cli = CalculadoraCLI()
        cli.ejecutar()
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
