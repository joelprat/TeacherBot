#include <Ethernet.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED }; // Dirección MAC del Arduino
IPAddress serverIP(127, 0, 0, 1); // Dirección IP del servidor
int serverPort = 1234; // Puerto del servidor

EthernetClient client;

void setup() {
  Ethernet.begin(mac);
  delay(1000);
  Serial.begin(9600);
}

void loop() {
  if (client.connect(serverIP, serverPort)) {
    // Conexión establecida
    Serial.println("Conexión establecida al servidor");

    // Enviar datos al servidor
    String data = "Datos desde Arduino";
    client.println(data);

    // Esperar la respuesta del servidor
    while (client.available()) {
      String response = client.readStringUntil('\r');
      Serial.println("Respuesta del servidor: " + response);
    }

    // Cerrar la conexión
    client.stop();
    Serial.println("Conexión cerrada");
  } else {
    // No se pudo establecer la conexión
    Serial.println("No se pudo conectar al servidor");
  }

  delay(5000);
}