"""
TESTS DE INTEGRACIÓN - Server y Cliente Refactorizados
=======================================================
Pruebas de integración para las versiones refactorizadas

Cubre:
- Conexión real cliente-servidor
- Envío y recepción de mensajes
- Broadcast a múltiples clientes simultáneos
- Comunicación bidireccional con callbacks
"""

import pytest
import socket
import threading
import time
from server import ServidorChat
from cliente import ClienteChat


def test_integracion_broadcast_multiples_clientes():
    """
    INTEGRACIÓN: Servidor hace broadcast a múltiples clientes conectados
    
    Flujo:
    1. Conectar 3 clientes
    2. Cliente 1 envía mensaje
    3. Servidor hace broadcast
    4. Clientes 2 y 3 reciben el mensaje
    
    Integra: ServidorChat.broadcast() + handle_cliente() + ClienteChat conexión real
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
    
    # Iniciar recepción en clientes 2 y 3
    mensajes_c2 = []
    mensajes_c3 = []
    
    def callback_c2(msg):
        mensajes_c2.append(msg)
    
    def callback_c3(msg):
        mensajes_c3.append(msg)
    
    thread_c2 = threading.Thread(target=cliente2.recibir_mensajes, args=(callback_c2,), daemon=True)
    thread_c3 = threading.Thread(target=cliente3.recibir_mensajes, args=(callback_c3,), daemon=True)
    thread_c2.start()
    thread_c3.start()
    time.sleep(0.3)
    
    # Cliente 1 envía mensaje
    cliente1.enviar_mensaje("Mensaje de broadcast")
    time.sleep(1.5)
    
    # Verificar que clientes 2 y 3 recibieron el mensaje
    assert len(mensajes_c2) > 0, "Cliente 2 debería recibir mensajes"
    assert len(mensajes_c3) > 0, "Cliente 3 debería recibir mensajes"
    
    # Verificar que el mensaje llegó
    mensajes_c2_str = ' '.join(mensajes_c2)
    mensajes_c3_str = ' '.join(mensajes_c3)
    
    assert "Mensaje de broadcast" in mensajes_c2_str
    assert "Mensaje de broadcast" in mensajes_c3_str
    
    print(f"✓ Broadcast exitoso - Cliente 2 recibió {len(mensajes_c2)} mensajes")
    print(f"✓ Broadcast exitoso - Cliente 3 recibió {len(mensajes_c3)} mensajes")
    
    # Cleanup
    cliente1.desconectar()
    cliente2.desconectar()
    cliente3.desconectar()
    time.sleep(0.5)
    servidor.detener()


# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
