import socket
import threading


class ClienteChat:
    """Cliente de chat refactorizado para testing"""
    
    def __init__(self, host='127.0.0.1', port=55123):
        """
        Args:
            host: IP del servidor
            port: Puerto del servidor
        """
        self.host = host
        self.port = port
        self.socket = None
        self.conectado = False
        self.mensajes_recibidos = []
    
    def conectar(self):
        """
        Returns:
            bool: True si conectó exitosamente, False si falló
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.conectado = True
            return True
        except ConnectionRefusedError as e:
            print(f"No se pudo conectar al servidor: {e}")
            self.conectado = False
            return False
    
    def enviar_mensaje(self, mensaje):
        """
        Args:
            mensaje (str): Mensaje a enviar
        Returns:
            bool: True si se envió exitosamente
        """
        if not self.conectado or not self.socket:
            return False
        
        try:
            self.socket.send(mensaje.encode())
            return True
        except (ConnectionResetError, OSError) as e:
            print(f"Error enviando mensaje: {e}")
            self.conectado = False
            return False
    
    def recibir_mensajes(self):
        """
        Recibe mensajes del servidor (bloqueante) y los almacena en self.mensajes_recibidos.
        Imprime cada mensaje recibido. Retorna el último mensaje recibido o None si la conexión se cierra.
        """
        ultimo = None
        try:
            while self.conectado:
                mensaje = self.socket.recv(1024)
                if not mensaje:
                    print("Conexión cerrada por el servidor.")
                    self.conectado = False
                    break
                texto = mensaje.decode()
                self.mensajes_recibidos.append(texto)
                print(texto)
                ultimo = texto
            return ultimo
        except (ConnectionAbortedError, ConnectionResetError, OSError) as e:
            if self.conectado:
                print(f"Error en recepción: {e}")
            self.conectado = False
            return None
        finally:
            self.desconectar()
    

    
    def salir(self):
        """Envía mensaje de salida y desconecta"""
        self.enviar_mensaje("Usuario ha salido del chat.")
        self.desconectar()
    
    def desconectar(self):
        """Cierra la conexión"""
        self.conectado = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass



if __name__ == "__main__":
    cliente = ClienteChat()
    
    if not cliente.conectar():
        exit()
    
    print("Te has conectado al servidor, ya puedes escribir")
    
    # Iniciar recepción en hilo separado
    thread = threading.Thread(target=cliente.recibir_mensajes, daemon=True)
    thread.start()
    
    # Loop de envío
    try:
        while cliente.conectado:
            mensaje = input()
            
            if mensaje.lower() == "/salir":
                cliente.salir()
                break
            
            if not cliente.enviar_mensaje(mensaje):
                print("Error al enviar mensaje")
                break
                
    except KeyboardInterrupt:
        print("\nCerrando cliente por interrupción...")
        cliente.desconectar()
