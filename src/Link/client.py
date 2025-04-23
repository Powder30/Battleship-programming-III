from connection import Conexion



def main():
    
    # Cambiar modo_servidor a False, ya que el cliente se conecta al servidor
    red = Conexion(modo_servidor=False, ip = "244.178.44.111", puerto=5500)  # Cambia esta IP a la del servidor

    while True:
        # Enviar un mensaje al servidor
        mensaje = input("Escribe un mensaje: ")
        red.enviar_datos({"mensaje": mensaje})

        # Recibir respuesta del servidor
        respuesta = red.recibir_datos()
        print("Servidor dice:", respuesta["mensaje"])

main()
