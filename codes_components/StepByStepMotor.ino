// Configuración de pines
const int stepPin = 6;     // Pin STEP conectado al pin 9 del Arduino
const int dirPin = 7;      // Pin DIR conectado al pin 3 del Arduino

void setup() {
  // Configurar los pines como salidas
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

void loop() {
  digitalWrite(dirPin, HIGH);  // Establecer la dirección del giro (HIGH o LOW)

  // Generar 2000 pulsos para hacer que el motor gire
  for (int i = 0; i < 2000; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);    // Retardo para la duración del pulso
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);    // Retardo entre pulsos
  }

  delay(1000);  // Retardo de 1 segundo antes de invertir la dirección
  digitalWrite(dirPin, LOW);  // Invertir la dirección del giro

  // Generar 2000 pulsos para hacer que el motor gire en la dirección opuesta
  for (int i = 0; i < 2000; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);    // Retardo para la duración del pulso
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);    // Retardo entre pulsos
  }

  delay(1000);  // Retardo de 1 segundo antes de repetir el ciclo
}
