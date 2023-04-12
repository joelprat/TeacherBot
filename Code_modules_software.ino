#include <LiquidCrystal.h>
#include <Servo.h>

// Inicializar la biblioteca de la pantalla LCD
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

Servo servo1;
// Define las constantes de los pines
const int motorPin = 13;
const int encoderPinA = 2;
const int encoderPinB = 3;

// Define la variable para almacenar la posición del encoder
volatile long encoderPos = 0;

// Interrupción que se ejecuta cuando el encoder gira
void handleEncoder() {
  if (digitalRead(encoderPinA) == digitalRead(encoderPinB)) {
    encoderPos++;
  } else {
    encoderPos--;
  }
}

void setup() {
  // Configura los pines como entrada/salida
  pinMode(motorPin, OUTPUT);
  pinMode(encoderPinA, INPUT);
  pinMode(encoderPinB, INPUT);
   lcd.begin(16, 2);
  // Imprimir un mensaje en la pantalla LCD
  lcd.print("Hola, Tinkercad!");
  
  servo1.attach(6);
  servo1.write(0);
  
  // Activa la interrupción del encoder
  attachInterrupt(digitalPinToInterrupt(encoderPinA), handleEncoder, CHANGE);
  
  // Configura la velocidad del motor
  // (ajusta este valor según tus necesidades)
  analogWrite(motorPin, 100);
}

void loop() {
  // Muestra la posición actual del encoder en el monitor serie
  Serial.println(encoderPos);
  
  // Activa el motor durante 1 segundo
  digitalWrite(motorPin, HIGH);
  delay(1000);
  digitalWrite(motorPin, LOW);
  delay(1000);
  
   //funcionamiento servo
  for(int i=0; i <= 180; i++){
    servo1.write(i);
    delay(15); 
  }
}
