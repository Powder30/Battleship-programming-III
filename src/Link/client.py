from connection import Conexion
import sys
import threading



def main():
    try:
        red = Conexion(modo_servidor=False, ip="192.168.1.101", puerto=5500)  # Usa la IP del servidor
    except ConnectionError as e:
        print(f"[ERROR CLIENTE]: No se pudo conectar al servidor: {e}")
        sys.exit()

    print("[CLIENTE] Conectado al servidor. Iniciando chat.")

    while True:
        # Enviar un mensaje al servidor
        mensaje_cliente = input("[CLIENTE (Tú)] Escribe tu mensaje: ")
        red.enviar_datos({"mensaje": mensaje_cliente})

        # Recibir respuesta del servidor
        respuesta = red.recibir_datos()
        if not respuesta:
            print("[CLIENTE] El servidor se ha desconectado.")
            break  # Salir del bucle si el servidor se desconecta

        mensaje_servidor = respuesta.get("mensaje")
        if mensaje_servidor:
            print(f"[SERVIDOR]: {mensaje_servidor}")
        else:
            print("[CLIENTE] Respuesta del servidor sin el campo 'mensaje'.")

    print("[CLIENTE] Fin de la comunicación.")
    red.finalizar()
if __name__ == "__main__":
    main()

