#!/usr/bin/env python3
"""
Ejemplo de uso de la calculadora de gastos compartidos.
Este script demuestra las funcionalidades principales del sistema.
"""

from models.persona import Persona
from models.gasto import Gasto
from models.grupo import Grupo
from services.balance_service import BalanceService
from services.simplificador_service import SimplificadorService


def ejemplo_viaje_grupo():
    """Ejemplo: Viaje de un grupo de amigos."""
    print("🗺️ EJEMPLO: Viaje de un grupo de amigos")
    print("=" * 50)
    
    # Crear personas
    alice = Persona("Alice")
    bob = Persona("Bob")
    charlie = Persona("Charlie")
    diana = Persona("Diana")
    
    print(f"👥 Personas creadas:")
    for persona in [alice, bob, charlie, diana]:
        print(f"   • {persona}")
    
    # Crear grupo
    grupo = Grupo("Viaje a la Montaña")
    grupo.agregar_miembro(alice)
    grupo.agregar_miembro(bob)
    grupo.agregar_miembro(charlie)
    grupo.agregar_miembro(diana)
    
    print(f"\n🏔️ Grupo creado: {grupo}")
    
    # Registrar gastos
    gastos = [
        Gasto(alice, 400.0, "Hotel por 2 noches", [alice, bob, charlie, diana]),
        Gasto(bob, 120.0, "Gasolina", [alice, bob, charlie, diana]),
        Gasto(charlie, 80.0, "Cena del viernes", [alice, bob, charlie, diana]),
        Gasto(diana, 60.0, "Almuerzo del sábado", [alice, bob, charlie, diana]),
        Gasto(alice, 40.0, "Snacks para el viaje", [alice, bob, charlie, diana]),
        Gasto(bob, 32.0, "Entradas al museo", [bob, charlie, diana]),  # Alice no fue
        Gasto(charlie, 24.0, "Helados", [charlie, diana])  # Solo Charlie y Diana
    ]
    
    print(f"\n💸 Gastos registrados:")
    for i, gasto in enumerate(gastos, 1):
        print(f"{i}. {gasto}")
        grupo.agregar_gasto(gasto)
    
    # Calcular balances
    balance_service = BalanceService()
    balances = balance_service.calcular_balance_grupo(grupo)
    
    print(f"\n💰 BALANCES INDIVIDUALES:")
    print("-" * 30)
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
    
    print(f"\n🔄 SIMPLIFICACIÓN DE DEUDAS:")
    print("-" * 35)
    if transferencias:
        print("💸 Transferencias necesarias:")
        for i, transferencia in enumerate(transferencias, 1):
            print(f"{i}. {transferencia}")
    else:
        print("🎉 ¡No hay deudas que simplificar!")
    
    # Mostrar métricas de eficiencia
    eficiencia = simplificador.calcular_eficiencia_simplificacion(grupo)
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   • Deudas originales: {eficiencia['deudas_originales']}")
    print(f"   • Transferencias necesarias: {eficiencia['transferencias_necesarias']}")
    print(f"   • Reducción: {eficiencia['reduccion_porcentaje']:.1f}%")
    print(f"   • Monto total a transferir: ${eficiencia['monto_total_transferencias']:.2f}")


def ejemplo_deudas_cruzadas():
    """Ejemplo: Deudas cruzadas complejas."""
    print("\n\n🔄 EJEMPLO: Deudas cruzadas complejas")
    print("=" * 50)
    
    # Crear personas
    alice = Persona("Alice")
    bob = Persona("Bob")
    charlie = Persona("Charlie")
    
    # Crear grupo
    grupo = Grupo("Gastos Cruzados")
    grupo.agregar_miembro(alice)
    grupo.agregar_miembro(bob)
    grupo.agregar_miembro(charlie)
    
    # Crear deudas cruzadas
    gastos = [
        Gasto(alice, 30.0, "Alice paga por todos", [alice, bob, charlie]),
        Gasto(bob, 30.0, "Bob paga por todos", [alice, bob, charlie]),
        Gasto(charlie, 30.0, "Charlie paga por todos", [alice, bob, charlie]),
    ]
    
    print(f"💸 Gastos que crean deudas cruzadas:")
    for gasto in gastos:
        print(f"   • {gasto}")
        grupo.agregar_gasto(gasto)
    
    # Calcular balances
    balance_service = BalanceService()
    balances = balance_service.calcular_balance_grupo(grupo)
    
    print(f"\n💰 Balances después de gastos cruzados:")
    for persona, balance in balances.items():
        if abs(balance) < 0.01:
            print(f"⚪ {persona.nombre}: Balance equilibrado (${balance:.2f})")
    
    # Simplificar deudas
    simplificador = SimplificadorService(balance_service)
    transferencias = simplificador.simplificar_deudas(grupo)
    
    print(f"\n🔄 Resultado de la simplificación:")
    if not transferencias:
        print("🎉 ¡Perfecto! Las deudas se cancelan entre sí. No se necesitan transferencias.")
    else:
        print("💸 Transferencias necesarias:")
        for transferencia in transferencias:
            print(f"   • {transferencia}")


def ejemplo_gasto_personal():
    """Ejemplo: Gasto personal que no afecta a otros."""
    print("\n\n👤 EJEMPLO: Gasto personal")
    print("=" * 35)
    
    # Crear personas
    alice = Persona("Alice")
    bob = Persona("Bob")
    
    # Crear grupo
    grupo = Grupo("Gastos Personales")
    grupo.agregar_miembro(alice)
    grupo.agregar_miembro(bob)
    
    # Alice paga algo solo para ella
    gasto_personal = Gasto(
        pagador=alice,
        monto=25.0,
        descripcion="Comida personal de Alice",
        beneficiarios=[alice]  # Solo Alice se beneficia
    )
    
    print(f"💸 Gasto personal:")
    print(f"   • {gasto_personal}")
    grupo.agregar_gasto(gasto_personal)
    
    # Calcular balances
    balance_service = BalanceService()
    balances = balance_service.calcular_balance_grupo(grupo)
    
    print(f"\n💰 Balances:")
    for persona, balance in balances.items():
        if abs(balance) < 0.01:
            print(f"⚪ {persona.nombre}: Balance equilibrado (${balance:.2f})")
        else:
            print(f"🔴 {persona.nombre}: Debe ${balance:.2f}")
    
    print(f"\n💡 Explicación: Como Alice pagó solo para ella, no hay deudas entre personas.")


def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("🧮 CALCULADORA DE GASTOS COMPARTIDOS")
    print("=" * 50)
    print("Ejemplos de uso del sistema\n")
    
    # Ejecutar ejemplos
    ejemplo_viaje_grupo()
    ejemplo_deudas_cruzadas()
    ejemplo_gasto_personal()
    
    print(f"\n" + "=" * 50)
    print("✅ Todos los ejemplos ejecutados correctamente!")
    print("💡 Para usar la interfaz interactiva, ejecuta: python cli.py")


if __name__ == "__main__":
    main()
