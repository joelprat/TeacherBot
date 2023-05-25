#include <SoftwareSerial.h>
const int ledPin = 13;
int incomingByte = 0;
String readString;
SoftwareSerial BTSerial(10, 11);   // RX | TX
void setup() {
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
    if (readString.length() > 0){
      digitalWrite(ledPin, HIGH);
      readString = "";
    }
  delay(1000); //a little delay is needed so you can see the

}