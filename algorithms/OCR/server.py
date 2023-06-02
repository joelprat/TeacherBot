import socket
import utils as m
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
    while True:
        server_socket.listen(1)
        print("Esperando conexiones...")
        client_socket, addr = server_socket.accept()
        print(f"Conexión establecida desde {addr}")
        # Enviar una respuesta al cliente        
        data=""
        received_data= ""
        while data != "DICTA" and data != "DICTAF" and data.split(" ")[0] != "IMG":
            data = m.recibir_todo(client_socket)            
            print("MSG RECV")
            data = data.decode("utf-8")           
       
        
        if data == "DICTA" :
            num_palabras = faker.random_int(min=10, max=15)  # Genera un número aleatorio de palabras entre 10 y 15
            frase = ""
            
            for i in range(5):   
                frase += faker.word()+". "
            traduccion = m.traducir(frase, idioma_origen, idioma_destino)           

            msg = "DICTA:"+traduccion
            client_socket.send(msg.encode())
            print(msg)
        
        if data == "DICTAF" :            
            frase = m.obtener_frase_aleatoria()                       
            traduccion = frase
            msg = "DICTA:"+traduccion
            client_socket.send(msg.encode())
            print(msg)

        if data.split(" ")[0] == "IMG":
            img= data.split(" ")[1]
            img += "=" * (4 - (len(img) % 4))  # Ag            
            imagen_bytes = base64.b64decode(img)
            ruta_archivo = "imagen.jpeg"  # Proporciona la ruta y el nombre del archivo           
            with open(ruta_archivo, "wb") as archivo:
                archivo.write(imagen_bytes)           
            mov = r.robot_movement()
            response = "START:-45|0;"
            for i in mov:
                for j in i:                    
                    response += str(j[0])+"|"+str(j[1])+";" 
            response +="0|0;END\n"        
            
            print(response)
            client_socket.send(response.encode())        
      
        client_socket.close()

        

    
    server_socket.close()
