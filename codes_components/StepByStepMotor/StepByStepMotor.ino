#include <AccelStepper.h>
// Configuración de pines
const int stepPin = 6;     // Pin STEP conectado al pin 6 del Arduino
const int dirPin = 7;      // Pin DIR conectado al pin 7 del Arduino
AccelStepper stepper(AccelStepper::DRIVER, stepPin, dirPin);
void setup() {
  // Configurar los pines como salidas
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  stepper.setMaxSpeed(100);         // Velocidad máxima en pasos por segundo
  stepper.setAcceleration(100);      // Aceleración en pasos por segundo por segundo
  //stepper.setSpeed(500);             // Velocidad inicial en pasos por segundo
  stepper.moveTo(10);
}

void loop() {

  
  digitalWrite(dirPin, HIGH);  // Invertir la dirección del giro
  
  float pasosObjetivo = 180 * 2000.0 / 360.0;
  /* Generar 2000 pulsos para hacer que el motor gire en la dirección opuesta
  for (int i = 0; i < pasosObjetivo; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);    // Retardo para la duración del pulso
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);    // Retardo entre pulsos
  }*/
  if(stepper.distanceToGo() == 0){
    delay(1000);
    stepper.move(15);
  }else{
    stepper.run();
  }
  /*stepper.moveTo(100);  // Número de pasos a mover
  stepper.runToPosition();
  delay(1000);*/
 // delay(1000);  // Retardo de 1 segundo antes de repetir el ciclo
}
