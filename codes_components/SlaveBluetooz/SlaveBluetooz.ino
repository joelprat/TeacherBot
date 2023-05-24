#include <SoftwareSerial.h>

SoftwareSerial BTSerial(2, 3); // RX, TX pins del módulo Bluetooth

void setup() {
  Serial.begin(9600);
  Serial.println("ENTER AT Commands:");
  BTSerial.begin(9600);
  //sendATCommand("AT+NAME=RobotTecher1");
  //delay(500);
  //sendATCommand("AT+BAUD4");
  
}

void loop() {
  // Verificar si se ha recibido una respuesta desde el dispositivo Bluetooth
  //Write data from HC06 to Serial Monitor
  if (BTSerial.available()){
    Serial.write(BTSerial.read());
  }
  
  //Write from Serial Monitor to HC06
  if (Serial.available()){
    BTSerial.write(Serial.read());
  }  
}

void sendATCommand(const char* command) {
  BTSerial.println(command);
}
