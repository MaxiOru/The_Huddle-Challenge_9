"""SERVER REFACTORIZADO - Versión testeable"""

import socket
import threading


class ServidorChat:
    def __init__(self, host='127.0.0.1', port=55123):
        self.host = host
        self.port = port
        self.clientes = []
        self.servidor = None
        self.activo = False
    
    def validar_mensaje(self, mensaje):
        return bool(mensaje and mensaje.strip())
    
    def broadcast(self, mensaje, excluir_cliente=None):
        enviados = 0
        for cliente in self.clientes[:]:
            if cliente == excluir_cliente:
                continue
            try:
                cliente.send(mensaje)
                enviados += 1
            except (BrokenPipeError, ConnectionResetError, OSError):
                self.remover_cliente(cliente)
        return enviados
    
    def remover_cliente(self, cliente):
        if cliente in self.clientes:
            self.clientes.remove(cliente)
            try:
                cliente.close()
            except:
                pass
    
    def agregar_cliente(self, cliente):
        if cliente not in self.clientes:
            self.clientes.append(cliente)
    
    def handle_cliente(self, cliente, direccion):
        try:
            while self.activo:
                mensaje = cliente.recv(1024)
                if not mensaje:
                    self.broadcast(f"{direccion} se desconectó.".encode())
                    break
                
                texto = mensaje.decode()
                if not self.validar_mensaje(texto):
                    cliente.send("[ERROR] Mensaje vacío.".encode())
                    continue
                
                if texto == "Usuario ha salido del chat.":
                    self.broadcast(f"{direccion} dejó el chat.".encode())
                    break
                
                self.broadcast(f"{direccion}: {texto}".encode())
                
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            self.broadcast(f"{direccion} se desconectó.".encode())
        finally:
            self.remover_cliente(cliente)
    
    def iniciar(self):
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.servidor.bind((self.host, self.port))
        self.servidor.listen()
        self.activo = True
        print(f"Servidor escuchando en {self.host}:{self.port}")
    
    def aceptar_conexiones(self):
        try:
            while self.activo:
                cliente, direccion = self.servidor.accept()
                print(f"Conectado con {direccion}")
                self.agregar_cliente(cliente)
                self.broadcast(f"{direccion} se ha conectado".encode())
                threading.Thread(target=self.handle_cliente, args=(cliente, direccion), daemon=True).start()
        except OSError as e:
            if self.activo:
                print(f"Error: {e}")
    
    def detener(self):
        self.activo = False
        for cliente in self.clientes[:]:
            self.remover_cliente(cliente)
        if self.servidor:
            try:
                self.servidor.close()
            except:
                pass


if __name__ == "__main__":
    servidor = ServidorChat()
    servidor.iniciar()
    print("Para cerrar el servidor presiona Ctrl+C")
    try:
        servidor.aceptar_conexiones()
    except KeyboardInterrupt:
        print("\nCerrando servidor...")
        servidor.detener()
