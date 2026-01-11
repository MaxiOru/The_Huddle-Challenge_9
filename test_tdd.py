"""
PRUEBA TDD Validación de mensajesS
Se prueba la función validar_mensaje() de la clase ServidorChat en server.py
"""
import pytest
from server import ServidorChat

# Función probada: ServidorChat.validar_mensaje()
def test_validar_mensaje_con_contenido():
    """
    Ciclo seguido:
    1. RED: Test escrito primero, falló (método no existía)
    2. GREEN: Implementamos validar_mensaje() básico
    3. REFACTOR: Optimizado para manejar vacíos, espacios y None
    
    Funcionalidad:
    - Acepta mensajes con contenido y rechaza mensajes vacíos, solo espacios y None
    """
    servidor = ServidorChat()
    
    # Caso positivo: mensaje válido debe ser aceptado
    resultado = servidor.validar_mensaje("Hola")
    assert resultado == True
    
    # Casos negativos: mensajes inválidos deben ser rechazados
    assert servidor.validar_mensaje("") == False
    assert servidor.validar_mensaje("   ") == False
    assert servidor.validar_mensaje(None) == False 


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
