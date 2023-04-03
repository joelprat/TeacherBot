// Incluir la librería de la biblioteca Servo
#include <Servo.h>

// Crear un objeto de tipo Servo
Servo myservo;

void setup() {
  // Establecer el pin del servo
  myservo.attach(9);
}

void loop() {
  // Mover el servo a 0 grados
  myservo.write(0);
  delay(1000);

  // Mover el servo a 90 grados
  myservo.write(90);
  delay(1000);

  // Mover el servo a 180 grados
  myservo.write(180);
  delay(1000);
}
