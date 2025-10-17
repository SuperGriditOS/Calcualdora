#!/usr/bin/env python3
"""
Demo de la interfaz web - Crea datos de ejemplo para probar la aplicación.
"""

from models.persona import Persona
from models.gasto import Gasto
from models.grupo import Grupo
from services.balance_service import BalanceService
from services.simplificador_service import SimplificadorService

def crear_datos_demo():
    """Crea datos de ejemplo para demostrar la interfaz web."""
    print("🎭 Creando datos de demostración...")
    
    # Crear personas
    alice = Persona("Alice")
    bob = Persona("Bob")
    charlie = Persona("Charlie")
    diana = Persona("Diana")
    eva = Persona("Eva")
    
    print(f"👥 Personas creadas: {[p.nombre for p in [alice, bob, charlie, diana, eva]]}")
    
    # Crear grupo
    grupo = Grupo("Viaje de Fin de Semana")
    for persona in [alice, bob, charlie, diana, eva]:
        grupo.agregar_miembro(persona)
    
    print(f"🏔️ Grupo creado: {grupo.nombre}")
    
    # Crear gastos variados
    gastos = [
        Gasto(alice, 500.0, "Hotel por 2 noches", [alice, bob, charlie, diana, eva]),
        Gasto(bob, 150.0, "Gasolina ida y vuelta", [alice, bob, charlie, diana, eva]),
        Gasto(charlie, 200.0, "Cena del viernes", [alice, bob, charlie, diana, eva]),
        Gasto(diana, 120.0, "Almuerzo del sábado", [alice, bob, charlie, diana, eva]),
        Gasto(eva, 80.0, "Desayuno del domingo", [alice, bob, charlie, diana, eva]),
        Gasto(alice, 60.0, "Snacks para el viaje", [alice, bob, charlie, diana, eva]),
        Gasto(bob, 90.0, "Entradas al museo", [bob, charlie, diana]),  # Eva y Alice no fueron
        Gasto(charlie, 45.0, "Helados", [charlie, diana]),  # Solo Charlie y Diana
        Gasto(diana, 75.0, "Recuerdos", [diana]),  # Solo Diana
        Gasto(eva, 100.0, "Actividades acuáticas", [eva, alice])  # Solo Eva y Alice
    ]
    
    print(f"💸 Gastos creados: {len(gastos)}")
    for i, gasto in enumerate(gastos, 1):
        print(f"   {i}. {gasto}")
        grupo.agregar_gasto(gasto)
    
    # Calcular balances
    balance_service = BalanceService()
    balances = balance_service.calcular_balance_grupo(grupo)
    
    print(f"\n💰 BALANCES FINALES:")
    for persona, balance in balances.items():
        if balance > 0.01:
            print(f"🔴 {persona.nombre}: Debe ${balance:.2f}")
        elif balance < -0.01:
            print(f"🟢 {persona.nombre}: Debe recibir ${abs(balance):.2f}")
        else:
            print(f"⚪ {persona.nombre}: Balance equilibrado")
    
    # Simplificar deudas
    simplificador = SimplificadorService(balance_service)
    transferencias = simplificador.simplificar_deudas(grupo)
    
    print(f"\n🔄 TRANSFERENCIAS SIMPLIFICADAS:")
    if transferencias:
        for i, transferencia in enumerate(transferencias, 1):
            print(f"   {i}. {transferencia}")
    else:
        print("   🎉 ¡No hay transferencias necesarias!")
    
    # Estadísticas
    eficiencia = simplificador.calcular_eficiencia_simplificacion(grupo)
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   • Deudas originales: {eficiencia['deudas_originales']}")
    print(f"   • Transferencias necesarias: {eficiencia['transferencias_necesarias']}")
    print(f"   • Reducción: {eficiencia['reduccion_porcentaje']:.1f}%")
    print(f"   • Monto total a transferir: ${eficiencia['monto_total_transferencias']:.2f}")
    
    return grupo

def main():
    """Función principal del demo."""
    print("🧮 Demo de la Calculadora de Gastos Compartidos")
    print("=" * 60)
    print("Este script crea datos de ejemplo para probar la interfaz web.\n")
    
    grupo = crear_datos_demo()
    
    print(f"\n" + "=" * 60)
    print("✅ Demo completado exitosamente!")
    print(f"\n💡 Para usar estos datos en la interfaz web:")
    print("   1. Ejecuta: python run_web.py")
    print("   2. Ve a 'Gestión de Grupos'")
    print("   3. Crea un grupo con el mismo nombre")
    print("   4. Agrega las mismas personas")
    print("   5. Registra los gastos mostrados arriba")
    print("\n🎯 O simplemente explora la interfaz web con tus propios datos!")

if __name__ == "__main__":
    main()
