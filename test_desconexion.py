"""
Pruebas que verifican el manejo de desconexiones en ServidorChat (server.py)
Funciones probadas: ServidorChat.broadcast(), ServidorChat.remover_cliente()
"""

import pytest
from unittest.mock import Mock
from server import ServidorChat

def test_broadcast_no_falla_con_cliente_desconectado():
    """
    DESCONEXIÓN: Verifica que broadcast() maneja errores sin bloquearse
    
    Requisito: "Los mensajes enviados por un cliente que se desconecta durante 
                la transmisión no causan errores en el sistema"
    """
    servidor = ServidorChat()

    cliente1 = Mock()
    cliente2 = Mock()  # Este va a fallar
    cliente3 = Mock()
    
    # Simular que cliente2 se desconecta durante el envío
    cliente2.send.side_effect = BrokenPipeError("Conexión rota")
    # Equivalente real: cliente.send() falla porque la conexión se cerró
    
    # Agregar a la lista del servidor
    servidor.clientes = [cliente1, cliente2, cliente3]
    
    # Ejecutar broadcast (NO debe lanzar excepción)
    mensaje = "Mensaje de prueba".encode()
    try:
        enviados = servidor.broadcast(mensaje)
    except Exception as e:
        pytest.fail(f"broadcast() no debe lanzar excepción, pero lanzó: {e}")
    
    # Verificar que cliente1 y cliente3 SÍ recibieron el mensaje
    cliente1.send.assert_called_once_with(mensaje)
    cliente3.send.assert_called_once_with(mensaje)
    
    # Verificar que cliente2 fue removido de la lista
    assert cliente2 not in servidor.clientes
    assert len(servidor.clientes) == 2 

    # Verificar que se retornó el número correcto de envíos exitosos
    assert enviados == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
