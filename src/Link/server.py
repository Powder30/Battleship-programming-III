from connection import Conexion

def main():
    # Cambiar modo_servidor a True, ya que el servidor espera conexiones
    red = Conexion(modo_servidor=True, ip="127.0.0.1", puerto=5500)  # Cambia esta IP a la del servidor
    
    while True:
        # Recibimos los datos del cliente
        datos = red.recibir_datos()
        print("Cliente dice:", datos["mensaje"])

        # Enviar una respuesta al cliente
        mensaje = input("Escribe un mensaje para enviar al cliente: ")
        red.enviar_datos({"mensaje": mensaje})

main()
