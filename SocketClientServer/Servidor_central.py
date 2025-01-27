import socket
import threading
#el servidor esta escuchando, por convención en el puerto 1025

comandos={"INSC","VIDEOS","INFO","DESCARGAR"}
##############################################################################################
#                               cmd_inscripcion
##############################################################################################
def cmd_inscripcion(solicitud):
    res="bien"
    if(len(solicitud)!=4):
        res="Formato de entrada incorrecto\nINSC nom_cliente IP puerto_escucha"
    return res
    
##############################################################################################
#                               cmd_videos
##############################################################################################    
def cmd_videos(solicitud):
    res="bien"
    if(len(solicitud)!=4):
        res="Formato de entrada incorrecto\nVIDEOS nom_cliente cantidad_videos lista_videos"
    return res
    
##############################################################################################
#                               cmd_info
##############################################################################################
def cmd_info(solicitud):
    res="bien"
    if(len(solicitud)!=1):
        res="Formato de entrada incorrecto\nINFO"
    return res
    
##############################################################################################
#                               cmd_descargar
##############################################################################################
def cmd_descargar(solicitud):
    res="bien"
    if(len(solicitud)!=2):
        res="Formato de entrada incorrecto\nDESCARGAR nom_video"
    else:
        1
    return res
        
##############################################################################################
#                               procesa_solicitud
##############################################################################################
def procesa_solicitud(solicitud):
    res="Comando desconocido"
    if(solicitud[0].upper() in comandos):
        if(solicitud[0].upper()=="INSC"):
            res=cmd_inscripcion(solicitud)
        if(solicitud[0].upper()=="VIDEOS"):
            res=cmd_videos(solicitud)
        if(solicitud[0].upper()=="INFO"):
            res=cmd_info(solicitud)
        if(solicitud[0].upper()=="DESCARGAR"):
            res=cmd_descargar(solicitud)
    return res
        
##############################################################################################
#                               manejar_cliente
##############################################################################################
def manejar_cliente(conn, addr):
    """Maneja la comunicación con un cliente específico."""
    print(f"Conexión establecida desde {addr}")
    with conn:
        while True:
            datos = conn.recv(1024).decode("utf-8")
            if not datos:  # Si no hay datos, el cliente cerró la conexión
                print(f"Conexión cerrada por el cliente {addr}")
                break
            respuesta=procesa_solicitud(datos.split())
            conn.send(respuesta.encode("utf-8"))
            
##############################################################################################
#                               servidor
##############################################################################################
def servidor():
    host = "0.0.0.0"  # Escucha en todas las interfaces disponibles
    puerto = 1025     # Puerto en el que escucha el servidor
    
    # Inicializamos el mapa_clientes donde se almacenarán los datos de los clientes
    mapa_clientes = {}

    # Abrir el archivo y cargar la información en el mapa_clientes
    try:
        with open("bd_clientes.txt", "r") as archivo:
            for linea in archivo:
                # Procesa la línea y actualiza el mapa_clientes
                # Aquí debes hacer el procesamiento según el formato de los datos
                # Asumimos que la información está en un formato adecuado, por ejemplo:
                cliente_info = linea.strip().split(',')  # Suponiendo que cada línea tiene el formato 'id, nombre, etc.'
                if len(cliente_info) > 1:
                    id_cliente = cliente_info[0]  # Asumiendo que el ID es el primer campo
                    datos_cliente = cliente_info[1:]  # El resto de la información
                    mapa_clientes[id_cliente] = datos_cliente  # Guarda los datos en el mapa_clientes

        print("Datos de clientes cargados correctamente.")
    except FileNotFoundError:
        print("Error: El archivo 'bd_clientes.txt' no fue encontrado.")
        return  # Salir si el archivo no existe

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, puerto))
        s.listen()
        print(f"Servidor escuchando en {host}:{puerto}")
        while True:
            conn, addr = s.accept()
            # Crea un nuevo hilo para manejar a cada cliente
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
            hilo.start()
##############################################################################################
#                               main
##############################################################################################
# Llamar a la función servidor si este script se ejecuta directamente
if __name__ == "__main__":
    servidor()
