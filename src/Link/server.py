from connection import Conexion


def main():
    
    # Cambiar modo_servidor a True, ya que el servidor espera conexiones
    red = Conexion(modo_servidor=True, ip = Conexion.get_local_ip(), puerto=5500)  # Cambia esta IP a la del servidor
    
   
    print("[SERVIDOR] Esperando a que un cliente se conecte...")
    print(f"[SERVIDOR] ip :  {Conexion.get_local_ip()} puerto : {5500}")
    red.connection_event.wait()  
    print("[SERVIDOR] Cliente conectado. Esperando mensajes...")
    while True:
        
        datos = red.recibir_datos()
        if not datos:
             print("[SERVIDOR] No se recibieron datos o el cliente se desconectó. Esperando nuevo mensaje...")
             break

        mensaje_cliente = datos.get("mensaje")
        if mensaje_cliente:
            print(f"[SERVIDOR] Cliente dice: {mensaje_cliente}")
            

        # Enviar una respuesta al cliente
            mensaje = input("Escribe un mensaje para enviar al cliente: ")
            red.enviar_datos({"mensaje": mensaje})
        else: 
            print("[SERVIDOR] Datos recibidos sin el campo 'mensaje'.")
    print("[SERVIDOR] Fin de la conexion...")      
    red.finalizar()  
if __name__ == "__main__":
    main()
