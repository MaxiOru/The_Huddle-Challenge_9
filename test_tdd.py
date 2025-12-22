"""
PRUEBAS TDD - ServidorChat.validar_mensaje()
=============================================
Pruebas siguiendo metodología Test-Driven Development para el servidor refactorizado.
Se prueba la función validar_mensaje() de la clase ServidorChat en server_refac.py

Ciclo: RED -> GREEN -> REFACTOR
"""

import pytest
from server import ServidorChat

# ============================================================================
# TDD: Validación de mensajes
# Ciclo: RED -> GREEN -> REFACTOR
# ============================================================================
# Función probada: ServidorChat.validar_mensaje()

# RED: ✓ La prueba falló inicialmente (validar_mensaje no existía)
# GREEN: ✓ Implementamos validar_mensaje() mínima en server_refac.py
# REFACTOR: ✓ Optimizado para manejar casos positivos y negativos

def test_validar_mensaje_con_contenido():
    """
    TDD COMPLETO: Validar que mensajes válidos sean aceptados
    
    Ciclo seguido:
    1. RED: Test escrito primero, falló (método no existía)
    2. GREEN: Implementamos validar_mensaje() básico
    3. REFACTOR: Optimizado para manejar vacíos, espacios y None
    
    Funcionalidad desarrollada con TDD:
    - Acepta mensajes con contenido válido
    - Rechaza mensajes vacíos, solo espacios y None
    """
    servidor = ServidorChat()
    
    # Caso positivo: mensaje válido debe ser aceptado
    resultado = servidor.validar_mensaje("Hola")
    assert resultado == True, "Mensaje con contenido debe ser aceptado"
    
    # Casos negativos: mensajes inválidos deben ser rechazados
    assert servidor.validar_mensaje("") == False, "Mensaje vacío debe ser rechazado"
    assert servidor.validar_mensaje("   ") == False, "Solo espacios debe ser rechazado"
    assert servidor.validar_mensaje(None) == False, "None debe ser rechazado"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
