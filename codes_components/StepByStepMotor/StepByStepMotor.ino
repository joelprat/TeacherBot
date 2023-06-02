#include <AccelStepper.h>
// Configuración de pines
const int stepPin = 6;     // Pin STEP conectado al pin 6 del Arduino
const int dirPin = 7;      // Pin DIR conectado al pin 7 del Arduino
const int stepPin2 = 3;     // Pin STEP conectado al pin 6 del Arduino
const int dirPin2 = 4; 
AccelStepper stepper(AccelStepper::DRIVER, stepPin, dirPin);
AccelStepper stepper2(AccelStepper::DRIVER, stepPin2, dirPin2);

// Incluir la librería de la biblioteca Servo
#include <Servo.h>

// Crear un objeto de tipo Servo
Servo myservo;
void setup() {
  // Configurar los pines como salidas
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  myservo.attach(13);
  stepper.setMaxSpeed(50);         // Velocidad máxima en pasos por segundo
  stepper.setAcceleration(50);      // Aceleración en pasos por segundo por segundo
  //stepper.setSpeed(500);             // Velocidad inicial en pasos por segundo
  stepper2.setMaxSpeed(100);         // Velocidad máxima en pasos por segundo
  stepper2.setAcceleration(100);
  int grau1 = 20;
  int grau2 = 90;
  int pasosObjetivo = grau1 * 800.0 / 360.0;
  int pasosObjetivo2 = grau2 * 800.0 / 360.0;
  //if(grau1<0){stepper.Direction(AccelStepper::DIRECTION_CW)}else{stepper.Direction(AccelStepper::DIRECTION_CCW)}
  //if(grau2<0){stepper2.Direction(AccelStepper::DIRECTION_CW)}else{stepper2.Direction(AccelStepper::DIRECTION_CCW)}
 // stepper.moveTo(pasosObjetivo);
  //stepper2.moveTo(pasosObjetivo2);
   myservo.write(0);
  int pasosMotor1[6] = {90};
  int pasosMotor2[6] = {0};
   for (int i = 0; i < 6; i++) {
      
      int pasosObjetivo = pasosMotor1[i] * 800.0 / 360.0;
      int pasosObjetivo2 = -pasosMotor2[i] * 800.0 / 360.0;
      
      stepper.moveTo(pasosObjetivo);
      stepper.runToPosition();
      
      // Mover el motor 2
      stepper2.moveTo(pasosObjetivo2);
      stepper2.runToPosition();
       while(stepper.distanceToGo() != 0 || stepper2.distanceToGo() != 0 ){
        if(stepper.distanceToGo() != 0 ){
          stepper.run();
        }
        if(stepper2.distanceToGo() != 0 ){
          stepper2.run();
        }          
       }
       delay(1000);
     if(i == 0 || i == 3){
          myservo.write(50);
        }
      if(i == 2 || i ==4){
        myservo.write(0);
      }
   //myservo.write(50);
   
  
    }
     myservo.write(0);
 
}

void loop() {

  
  digitalWrite(dirPin, HIGH);  // Invertir la dirección del giro
  
  
    /*
    // Mover el motor 1
    for (int i = 0; i < 2; i++) {
      
      int pasosObjetivo = pasosMotor1[i] * 800.0 / 360.0;
      int pasosObjetivo2 = pasosMotor2[i] * 800.0 / 360.0;
      stepper.moveTo(pasosObjetivo);
      stepper.runToPosition();

      // Mover el motor 2
      stepper2.moveTo(pasosObjetivo2);
      stepper2.runToPosition();
       while(stepper.distanceToGo() != 0 || stepper2.distanceToGo() != 0 ){
        if(stepper.distanceToGo() != 0 ){
          stepper.run();
        }
        if(stepper2.distanceToGo() != 0 ){
          stepper2.run();
        }          
       }
       delay(1000);
   //myservo.write(50);
   
   myservo.write(0);
    }
   */
  
  /*stepper.moveTo(100);  // Número de pasos a mover
  stepper.runToPosition();
  delay(1000);*/
 // delay(1000);  // Retardo de 1 segundo antes de repetir el ciclo
}
