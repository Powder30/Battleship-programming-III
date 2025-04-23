from connection import Conexion


def main():
    
    # Cambiar modo_servidor a True, ya que el servidor espera conexiones
    red = Conexion(modo_servidor=True, ip = Conexion.get_local_ip(), puerto=5555)  # Cambia esta IP a la del servidor
    
    while True:
        
        print("[SERVIDOR] Esperando a que un cliente se conecte...")
        print(f"[SERVIDOR] ip :  {Conexion.get_local_ip()} puerto : {5555}")
        red.connection_event.wait()  
        datos = red.recibir_datos()
        if not datos:
             print("[SERVIDOR] No se recibieron datos o el cliente se desconectó. Esperando nuevo mensaje...")
             continue

        print("Cliente dice:", datos.get("mensaje"))  # Usar .get() para evitar KeyError si la clave no existe

        # Enviar una respuesta al cliente
        mensaje = input("Escribe un mensaje para enviar al cliente: ")
        red.enviar_datos({"mensaje": mensaje})
        
if __name__ == "__main__":
    main()
