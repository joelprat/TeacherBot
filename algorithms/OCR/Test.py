import bluetooth

# Dirección MAC del dispositivo Bluetooth emparejado
device_address = "20:4:BD31CA"

try:
    # Conexión al dispositivo Bluetooth
    socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    socket.connect((device_address, 1))
    print("Conexión establecida con éxito.")

    # Aquí puedes enviar y recibir datos a través del socket Bluetooth

    # Cierra la conexión
    socket.close()

except bluetooth.BluetoothError as e:
    print("Error al conectar:", str(e))
