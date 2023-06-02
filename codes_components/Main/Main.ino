#include <SoftwareSerial.h>
#include <AccelStepper.h>
#include <String.h>
// Incluir la librería de la biblioteca Servo
#include <Servo.h>

// Crear un objeto de tipo Servo
Servo myservo;
const int ledPin = 13;
int incomingByte = 0;
const int stepPin = 6;     // Pin STEP conectado al pin 6 del Arduino
const int dirPin = 7;      // Pin DIR conectado al pin 7 del Arduino
const int stepPin2 = 3;     // Pin STEP conectado al pin 6 del Arduino
const int dirPin2 = 4; 
int start = 0;
float grau1, grau2;
String readString ,number1String ,number2String;
SoftwareSerial BTSerial(10, 11);   // RX | TX
AccelStepper stepper(AccelStepper::DRIVER, stepPin, dirPin);
AccelStepper stepper2(AccelStepper::DRIVER, stepPin2, dirPin2);
void setup() {
  // Configurar los pines como salidas
myservo.attach(13);
myservo.write(0);
pinMode(stepPin, OUTPUT);
pinMode(dirPin, OUTPUT);
pinMode(stepPin2, OUTPUT);
pinMode(dirPin2, OUTPUT);
stepper.setMaxSpeed(100);         // Velocidad máxima en pasos por segundo
stepper.setAcceleration(100); 
stepper2.setMaxSpeed(100);         // Velocidad máxima en pasos por segundo
stepper2.setAcceleration(100);
Serial.begin(9600);
pinMode(ledPin, OUTPUT);
BTSerial.begin(9600);

}

void loop() {
  while (BTSerial.available()) {
     delay(2); //delay to allow byte to arrive in input buffer
      char c = BTSerial.read();
      if (c != '\n'){
       readString += c;
      }
    }
    BTSerial.flush();
    if (readString.length() > 0){
      
       Serial.print("Envio: ");
       Serial.println(readString);
      if(readString == "START"){
        start = 1;
        //readString = "";
       
        
        }
      if(readString == "END"){
        start = 0;
        //readString = "";
        }
        if(readString == "PING"){
         myservo.write(50);
        //readString = "";
        delay(500);
        }
        if(readString == "PONG"){
         myservo.write(0);
        //readString = "";
        delay(500);
        }
      if(start == 1 && readString != "START" && readString != "PING" &&  readString != "PONG"){ 
        digitalWrite(ledPin, HIGH);     
        digitalWrite(dirPin, HIGH);  // Invertir la dirección del giro

        int separatorIndex = readString.indexOf('|');
        number1String = readString.substring(0, separatorIndex);
        number2String = readString.substring(separatorIndex + 1);
  
        // Convierte las cadenas de texto a números
        grau1 = number1String.toFloat();
        grau2 = number2String.toFloat();
        Serial.print("Grau1: ");
        Serial.println(number1String);
        Serial.print("Grau12 ");
        Serial.println(number2String);
        
        int pasosObjetivo1 = grau1 * 800 / 360.0;
        int pasosObjetivo2 = -grau2 * 800 / 360.0; 
        
        stepper.moveTo(pasosObjetivo1);
        stepper2.moveTo(pasosObjetivo2);
        while(stepper.distanceToGo() != 0 || stepper2.distanceToGo() != 0 ){
          if(stepper.distanceToGo() != 0 ){
            stepper.run();
          }
          if(stepper2.distanceToGo() != 0 ){
            stepper2.run();
          }          
        }
        delay(1000);
        
        
        readString = "";
        //delay(10000);  // Retardo de 1 segundo antes de repetir el ciclo
       }
        readString = "";
    }
   // delay(1000); //a little delay is needed so you can see the

}