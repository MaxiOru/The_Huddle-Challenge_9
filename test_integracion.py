"""
TEST DE INTEGRACIÓN - Servidor y Cliente

- Conexión real cliente-servidor
- Envío y recepción de mensajes
- Broadcast a múltiples clientes simultáneos
"""

import pytest
import socket
import threading
import time
from server import ServidorChat
from cliente import ClienteChat


def test_integracion_broadcast_multiples_clientes():
    """
    INTEGRACIÓN: El servidor hace broadcast a múltiples clientes conectados.

    Flujo:
    1. Conectar 3 clientes
    2. Cliente 1 envía mensaje
    3. Servidor hace broadcast
    4. Clientes 2 y 3 reciben el mensaje directamente

    Integra: ServidorChat.broadcast(), handle_cliente() y ClienteChat 
    """
    # Iniciar servidor
    servidor = ServidorChat(host='127.0.0.1', port=55125)
    servidor.iniciar()
    thread = threading.Thread(target=servidor.aceptar_conexiones, daemon=True)
    thread.start()
    time.sleep(0.3)
    
    # Crear 3 clientes y conectar
    cliente1 = ClienteChat(host='127.0.0.1', port=55125)
    cliente2 = ClienteChat(host='127.0.0.1', port=55125)
    cliente3 = ClienteChat(host='127.0.0.1', port=55125)
    
    assert cliente1.conectar() == True
    assert cliente2.conectar() == True
    assert cliente3.conectar() == True
    time.sleep(0.5)
    
    # Verificar que servidor tiene 3 clientes
    assert len(servidor.clientes) == 3
    
    # Cliente 1 envía mensaje
    cliente1.enviar_mensaje("Mensaje de broadcast")
    time.sleep(1.0)

    # Recibir mensajes en clientes 2 y 3
    recibido_c2 = cliente2.recibir_mensajes()
    recibido_c3 = cliente3.recibir_mensajes()

    assert recibido_c2 and "Mensaje de broadcast" in recibido_c2, "Cliente 2 no recibió el mensaje de broadcast"
    assert recibido_c3 and "Mensaje de broadcast" in recibido_c3, "Cliente 3 no recibió el mensaje de broadcast"

    print(f"✓ Broadcast exitoso - Cliente 2 recibió: {recibido_c2}")
    print(f"✓ Broadcast exitoso - Cliente 3 recibió: {recibido_c3}")
    
    # Cleanup
    cliente1.desconectar()
    cliente2.desconectar()
    cliente3.desconectar()
    time.sleep(0.5)
    servidor.detener()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
