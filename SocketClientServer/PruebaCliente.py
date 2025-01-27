import socket
import threading
import os
import queue

# Directorios para los videos
DIRECTORIO_VIDEOS = "./videos_compartidos"  # Videos disponibles para compartir
DIRECTORIO_RECIBIDOS = "./videos_recibidos"  # Videos descargados de otros clientes

# Crear los directorios si no existen
os.makedirs(DIRECTORIO_VIDEOS, exist_ok=True)
os.makedirs(DIRECTORIO_RECIBIDOS, exist_ok=True)

# Cola para manejar las descargas
cola_descargas = queue.Queue()

# ------------------------------
# Función para iniciar el servidor local
# ------------------------------
def iniciar_servidor_cliente():
    """
    Inicia un servidor local en el cliente para compartir videos con otros clientes.
    """
    def manejar_solicitud(conn, addr):
        """
        Maneja una solicitud de otro cliente para descargar un video.
        """
        try:
            with conn:
                datos = conn.recv(1024).decode("utf-8")
                if datos.startswith("DESCARGAR"):
                    video = datos.split()[1]
                    ruta_video = os.path.join(DIRECTORIO_VIDEOS, video)
                    if os.path.isfile(ruta_video):
                        tamano_archivo = os.path.getsize(ruta_video)
                        conn.sendall(f"{tamano_archivo}\n".encode("utf-8"))
                        with open(ruta_video, "rb") as archivo:
                            while (chunk := archivo.read(1024)):
                                conn.sendall(chunk)
                    else:
                        conn.sendall(b"ERROR El archivo solicitado no existe.\n")
        except Exception as e:
            print(f"Error manejando solicitud: {e}")

    puerto = 1030
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", puerto))
        puerto = s.getsockname()[1]
        print(f"Servidor del cliente escuchando en el puerto {puerto}")
        s.listen()
        while True:
            conn, addr = s.accept()
            hilo = threading.Thread(target=manejar_solicitud, args=(conn, addr))
            hilo.start()

# ------------------------------
# Función para procesar descargas en cola
# ------------------------------
def procesar_cola_descargas():
    """
    Procesa las descargas en cola de manera secuencial.
    """
    while True:
        host, puerto, video = cola_descargas.get()
        try:
            descargar_video(host, puerto, video)
        except Exception as e:
            print(f"Error en la descarga de '{video}': {e}")
        finally:
            cola_descargas.task_done()

# ------------------------------
# Función para descargar un video desde otro cliente
# ------------------------------
def descargar_video(host, puerto, video):
    """
    Descarga un video desde otro cliente.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect((host, puerto))
            s.sendall(f"DESCARGAR {video}".encode("utf-8"))

            buffer = b""
            while b"\n" not in buffer:
                buffer += s.recv(1024)
            respuesta = buffer.split(b"\n")[0].decode("utf-8")
            if respuesta.startswith("ERROR"):
                print(f"Error desde el servidor del cliente: {respuesta}")
                return

            tamano = int(respuesta)
            print(f"Tamaño del archivo: {tamano} bytes")
            with open(os.path.join(DIRECTORIO_RECIBIDOS, video), "wb") as archivo:
                bytes_recibidos = 0
                while bytes_recibidos < tamano:
                    datos = s.recv(1024)
                    if not datos:
                        break
                    archivo.write(datos)
                    bytes_recibidos += len(datos)
                    progreso = (bytes_recibidos / tamano) * 100
                    print(f"Descargando {video}: {int(progreso)}% completo")
            print(f"Video '{video}' descargado con éxito.")
    except Exception as e:
        print(f"Error al descargar el video '{video}': {e}")

# ------------------------------
# Hilo para escuchar notificaciones del servidor
# ------------------------------
def escuchar_notificaciones(s):
    """
    Escucha notificaciones enviadas por el servidor.
    """
    try:
        while True:
            notificacion = s.recv(1024).decode("utf-8")
            if notificacion == "SERVIDOR_CAIDO":
                print("El servidor se ha desconectado. Cerrando cliente...")
                exit(0)
            elif notificacion.startswith("El cliente"):
                print(f"Notificación del servidor: {notificacion}")
    except Exception as e:
        print(f"Error escuchando notificaciones: {e}")

# ------------------------------
# Función principal del cliente
# ------------------------------
def cliente():
    """
    Función principal para gestionar la interacción con el servidor y otros clientes.
    """
    hilo_servidor = threading.Thread(target=iniciar_servidor_cliente, daemon=True)
    hilo_servidor.start()

    hilo_cola_descargas = threading.Thread(target=procesar_cola_descargas, daemon=True)
    hilo_cola_descargas.start()

    host = "10.10.23.12"  # Cambia esto a la IP del servidor si no es local
    puerto = 1026

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, puerto))
            print(f"Conectado al servidor general en {host}:{puerto}")

            # Hilo para escuchar notificaciones del servidor
            hilo_notificaciones = threading.Thread(target=escuchar_notificaciones, args=(s,), daemon=True)
            hilo_notificaciones.start()

            while True:
                mensaje = input("Escribe un mensaje (o 'salir' para terminar): ")
                if mensaje.lower() == "salir":
                    print("Cerrando conexión...")
                    s.sendall("DESCONECTAR".encode("utf-8"))
                    break
                if mensaje.strip() == "":
                    continue
                s.sendall(mensaje.encode("utf-8"))
                respuesta = s.recv(1024).decode("utf-8")
                print(f"Respuesta del servidor: {respuesta}")

                if mensaje.upper().startswith("DESCARGAR"):
                    datos = respuesta.split()
                    if len(datos) >= 3 and datos[0] == "EXITO":
                        ip_cliente, puerto_cliente = datos[1], int(datos[2])
                        video = mensaje.split()[1]
                        cola_descargas.put((ip_cliente, puerto_cliente, video))
                        print(f"Descarga de '{video}' añadida a la cola.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Cliente finalizado.")

if __name__ == "__main__":
    cliente()
