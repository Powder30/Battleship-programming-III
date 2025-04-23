import socket
import json
import threading
import logging
if not logging.getLogger().hasHandlers():
  logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Conexion:
    @staticmethod
    def get_local_ip(): 
      ip_methods = [
            Conexion._get_ip_connect_external,
            Conexion._get_ip_socket_gethostbyname,
            Conexion._get_ip_fallback_localhost
        ]
      for method in ip_methods:
            try:
                ip = method()
                if ip and ip != '127.0.0.1':  # Evitar devolver localhost si otros métodos funcionan
                    logging.info(f"IP local obtenida con éxito: {ip} (usando {method.__name__})")
                    return ip
            except Exception as e:
                logging.error(f"Error al intentar obtener IP con {method.__name__}: {e}")
        
                logging.warning("No se pudo obtener una IP local válida. Usando fallback a 127.0.0.1")
                return '127.0.0.1'

    @staticmethod
    def _get_ip_connect_external():
        #Intenta obtener la IP conectándose a un servidor externo.
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except socket.error as e:
            logging.error(f"Método _get_ip_connect_external falló: {e}")
            raise

    @staticmethod
    def _get_ip_socket_gethostbyname():
        """Intenta obtener la IP usando hostname."""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return local_ip
        except socket.gaierror as e:
            logging.error(f"Método _get_ip_socket_gethostbyname falló: {e}")
            raise

    @staticmethod
    def _get_ip_fallback_localhost():
        #Método de fallback que siempre devuelve localhost.
        logging.info("Usando método de fallback para IP local: 127.0.0.1")
        return '127.0.0.1'
    def __init__(self, modo_servidor: bool, ip: str = "0.0.0.0", puerto: int = 5500):
        self.modo_servidor = modo_servidor
        self.ip = ip 
        self.puerto = puerto
        self.sock = None  
        self.canal = None
        self.connection_event = threading.Event()  
        if modo_servidor:
            self._iniciar_como_servidor()    
        else:  
            self._iniciar_como_cliente()

    def _iniciar_como_servidor(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.ip, self.puerto))
            print(f"[SERVIDOR] Escuchando en IP: {self.ip}  Puerto: {self.puerto}")
            self.sock.listen(1)
            print(f"[SERVIDOR] Esperando conexión en {self.ip}:{self.puerto}...")
            
            self.canal, direccion = self.sock.accept()
            self.connection_event.set()  
            print(f"[SERVIDOR] Cliente conectado desde {direccion}")
            
        except Exception as error:
            if self.sock:
                self.sock.close()
            raise ConnectionError(
                f"[ERROR SERVIDOR] No se pudo iniciar el servidor: {error}"
            )
            
     
    def _iniciar_como_cliente(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip, self.puerto))
            self.canal = self.sock
            print(f"[CLIENTE] Conectado al servidor en {self.ip}:{self.puerto}")
        except Exception as error:
            if self.sock:
               self.sock.close()
            raise ConnectionError(
                f"[ERROR CLIENTE] No se pudo conectar al servidor: {error}"
            )

    def enviar_datos(self, info: dict):
        try:
            mensaje = json.dumps(info).encode("utf-8")
            self.canal.sendall(mensaje)
        except Exception as error:
            print(f"[ERROR ENVÍO] {error}")

    def recibir_datos(self) -> dict:
        try:
            datos = self.canal.recv(1024).decode("utf-8")
            return json.loads(datos)
        except Exception as error:
            print(f"[ERROR RECEPCIÓN] {error}")
            return {}

    def finalizar(self):
        try:
            if self.canal:
                self.canal.close()
            self.sock.close()
            print("[CONEXIÓN] Cerrada exitosamente")
        except Exception as error:
            print(f"[ERROR AL CERRAR] {error}")
