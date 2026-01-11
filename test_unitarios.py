"""TESTS UNITARIOS 
Validación de mensajes, Gestión de clientes (agregar, remover, contar) y Broadcast básico

"""
import pytest
from unittest.mock import Mock
from server import ServidorChat

"""validar_mensaje() acepta mensajes con texto"""
def test_validar_mensaje_acepta_texto_valido():
    servidor = ServidorChat()
    assert servidor.validar_mensaje("Hola") == True
    assert servidor.validar_mensaje("Mensaje con espacios") == True

"""validar_mensaje() rechaza mensajes vacíos"""
def test_validar_mensaje_rechaza_vacios():
    servidor = ServidorChat()
    assert servidor.validar_mensaje("") == False
    assert servidor.validar_mensaje("   ") == False
    assert servidor.validar_mensaje(None) == False


"""agregar_cliente() añade cliente a la lista"""
def test_agregar_cliente():
    servidor = ServidorChat()
    cliente_mock = Mock()
    assert len(servidor.clientes) == 0
    servidor.agregar_cliente(cliente_mock)
    assert len(servidor.clientes) == 1
    assert cliente_mock in servidor.clientes


"""broadcast() envía mensaje a todos los clientes"""
def test_broadcast_envia_a_todos_los_clientes():
    servidor = ServidorChat()
    cliente1, cliente2, cliente3 = Mock(), Mock(), Mock()
    servidor.agregar_cliente(cliente1)
    servidor.agregar_cliente(cliente2)
    servidor.agregar_cliente(cliente3)
    
    mensaje = "Mensaje de prueba".encode()
    enviados = servidor.broadcast(mensaje)
    
    cliente1.send.assert_called_once_with(mensaje)
    cliente2.send.assert_called_once_with(mensaje)
    cliente3.send.assert_called_once_with(mensaje)
    assert enviados == 3

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])