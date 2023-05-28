import socket
import main as m
import robot_movement as r
import base64
# Configuración del servidor
HOST = '192.168.0.16'  # Dirección IP del servidor
PORT = 1234  # Puerto del servidor

# Crear un socket para el servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlazar el socket al HOST y PORT
server_socket.bind((HOST, PORT))

while True:
    """Generamos una frase o palabra rng"""
    idioma_origen = "en"
    idioma_destino = "ca"
    faker = m.Faker('en')  # Establece el idioma a catalán
    """num_palabras = faker.random_int(min=10, max=15)  # Genera un número aleatorio de palabras entre 10 y 15
    #frase = faker.sentence(nb_words=num_palabras)   
    frase = faker.word()
    traduccion = m.traducir(frase, idioma_origen, idioma_destino)


   Convertimos a audio la frase
    m.convertir_texto_a_audio(traduccion)"""

   
    # Escuchar conexiones entrantes
    #server_socket.listen(1)
    # print("Esperando conexiones...")

    # Aceptar una conexión entrante
    #client_socket, addr = server_socket.accept()
    #print(f"Conexión establecida desde {addr}")

    while True:
        server_socket.listen(1)
        print("Esperando conexiones...")
        client_socket, addr = server_socket.accept()
        print(f"Conexión establecida desde {addr}")
        # Enviar una respuesta al cliente
        #response = "FOTO\n"
        data=""
        received_data= ""
        while data != "DICTA" and data.split(" ")[0] != "IMG":
            data = m.recibir_todo(client_socket)
            #img = data;
            print("MSG RECV")
            data = data.decode("utf-8")
            #data = client_socket.recv(1024).decode("utf-8")
       
        #print(img)
        if data == "DICTA" :
            num_palabras = faker.random_int(min=10, max=15)  # Genera un número aleatorio de palabras entre 10 y 15
            #frase = faker.sentence(nb_words=num_palabras)   
            frase = faker.word()
            traduccion = m.traducir(frase, idioma_origen, idioma_destino)
            msg = "DICTA:"+traduccion
            client_socket.send(msg.encode())
            print(msg)

        if data.split(" ")[0] == "IMG":
            img= data.split(" ")[1]
            img += "=" * (4 - (len(img) % 4))  # Ag            
            imagen_bytes = base64.b64decode(img)
            #ruta_archivo = "imagen.jpeg"  # Proporciona la ruta y el nombre del archivo
            ruta_archivo = "test1.jpeg"
            with open(ruta_archivo, "wb") as archivo:
                archivo.write(imagen_bytes)           
            mov = r.robot_movement()
            response = "START:"
            for i in mov:
                for j in i:
                    #print(j)
                    response += str(j[0])+"|"+str(j[1])+";" 
            response +="END\n"        
            print(response)

            client_socket.send(response.encode())
        # Recibir datos del cliente
        #data = client_socket.recv(1024).decode()
        #if not data:
         #   break
        
        #print(f"Datos recibidos desde el cliente: {data}")
        client_socket.close()

        

    # Cerrar la conexión con el cliente
    #client_socket.close()

    # Cerrar el socket del servidor
    server_socket.close()
