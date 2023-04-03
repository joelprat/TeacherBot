#include <GoogleCloudSpeech.h>
#include <SoftwareSerial.h>

const int micPin = A0;
SoftwareSerial mySerial(3, 2); // RX, TX
GoogleCloudSpeech voice(mySerial);

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  while (!voice.setup()) {
    Serial.println("Waiting for voice recognition module to be ready...");
    delay(1000);
  }
  Serial.println("Voice recognition module ready!");
  voice.detect("hello world");
}

void loop() {
  if (voice.available()) {                          //Espera una palabra para ser detectada
    String speech = voice.getSpeech();
    Serial.println("Detected speech: " + speech);
  }
}
