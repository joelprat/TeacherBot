// Incluir la librería de la biblioteca Stepper
#include <Stepper.h>

// Definir el número de pasos por revolución
const int stepsPerRevolution = 200;

// Definir la secuencia de pasos
// Puedes modificar esta secuencia para cambiar la dirección del motor
int sequence[] = {0, 1, 2, 3};

// Inicializar el objeto Stepper
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

void setup() {
  // Establecer la velocidad del motor en pasos por segundo
  myStepper.setSpeed(50);
}

void loop() {
  // Hacer girar el motor en una dirección
  myStepper.step(100);
  delay(500);

  // Hacer girar el motor en la dirección opuesta
  myStepper.step(-100);
  delay(500);
}
