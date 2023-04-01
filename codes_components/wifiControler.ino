#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

// Cambia el nombre y la contraseña de tu red WiFi
const char* ssid = "nombre_de_la_red";
const char* password = "contraseña_de_la_red";

// Puerto UDP que se usará para la comunicación
unsigned int localUdpPort = 8888;

// Objeto WiFiUDP para manejar la comunicación UDP
WiFiUDP Udp;

void setup() {
  Serial.begin(9600);
  delay(10);

  // Conectar a la red WiFi
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Conexión WiFi establecida");
  Serial.print("Dirección IP obtenida: ");
  Serial.println(WiFi.localIP());

  // Inicializar el objeto WiFiUDP
  Udp.begin(localUdpPort);
  Serial.print("Escuchando en el puerto UDP ");
  Serial.println(localUdpPort);
}

void loop() {
  // Verificar si hay datos recibidos por UDP
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    Serial.print("Recibido ");
    Serial.print(packetSize);
    Serial.println(" bytes");

    // Leer los datos recibidos en un búfer
    char packetBuffer[packetSize];
    int len = Udp.read(packetBuffer, packetSize);
    if (len > 0) {
      packetBuffer[len] = 0;
    }
    Serial.print("Contenido: ");
    Serial.println(packetBuffer);

    // Convertir las coordenadas x,y recibidas a números
    int x = 0;
    int y = 0;
    sscanf(packetBuffer, "%d,%d", &x, &y);

    // Hacer algo con las coordenadas recibidas
    Serial.print("Coordenada x: ");
    Serial.println(x);
    Serial.print("Coordenada y: ");
    Serial.println(y);

    // Enviar un mensaje de confirmación
    char responseBuffer[] = "true";
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write(responseBuffer);
    Udp.endPacket();
    Serial.println("Mensaje de confirmación enviado");
  }

  // Agregar aquí cualquier otro código que deseas ejecutar en el loop()
}
