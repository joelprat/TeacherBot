const int microphonePin = A0; // Pin analógico del micrófono

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Leer el valor analógico del micrófono
  int microphoneValue = analogRead(microphonePin);

  // Imprimir el valor leído en el monitor serial
  Serial.print("Valor del micrófono: ");
  Serial.println(microphoneValue);

  // Agregar aquí cualquier otro código que deseas ejecutar en el loop()
}
