#include <SoftwareSerial.h>
#include <AccelStepper.h>
#include <String.h>
const int ledPin = 13;
int incomingByte = 0;
const int stepPin = 6;     // Pin STEP conectado al pin 6 del Arduino
const int dirPin = 7;      // Pin DIR conectado al pin 7 del Arduino
int start = 0;
float grau1, grau2;
String readString ,number1String ,number2String;
SoftwareSerial BTSerial(10, 11);   // RX | TX
AccelStepper stepper(AccelStepper::DRIVER, stepPin, dirPin);
void setup() {
  // Configurar los pines como salidas
pinMode(stepPin, OUTPUT);
pinMode(dirPin, OUTPUT);
stepper.setMaxSpeed(100);         // Velocidad máxima en pasos por segundo
stepper.setAcceleration(100); 
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
        readString = "";
        }
      if(readString == "END"){
        start = 0;
        readString = "";
        }
      if(start == 1 && readString != "START"){ 
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
        
        int pasosObjetivo1 = abs(grau1) * 200 / 360.0;
       
        stepper.moveTo(pasosObjetivo1);
        while(stepper.distanceToGo() != 0){
          stepper.run();
        }
        delay(1000);
        readString = "";
        //delay(10000);  // Retardo de 1 segundo antes de repetir el ciclo
            }
      }
   // delay(1000); //a little delay is needed so you can see the

}