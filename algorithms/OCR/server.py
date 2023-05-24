import socket

# Configuración del servidor
HOST = '192.168.0.16'  # Dirección IP del servidor
PORT = 1234  # Puerto del servidor

# Crear un socket para el servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlazar el socket al HOST y PORT
server_socket.bind((HOST, PORT))

while True:
    # Escuchar conexiones entrantes
    server_socket.listen(1)
    print("Esperando conexiones...")

    # Aceptar una conexión entrante
    client_socket, addr = server_socket.accept()
    print(f"Conexión establecida desde {addr}")

    while True:
        # Enviar una respuesta al cliente
        response = "FOTO\n"
        client_socket.send(response.encode())
        # Recibir datos del cliente
        data = client_socket.recv(1024).decode()
        if not data:
            break
        
        print(f"Datos recibidos desde el cliente: {data}")

        

    # Cerrar la conexión con el cliente
    client_socket.close()

    # Cerrar el socket del servidor
    server_socket.close()