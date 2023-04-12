#include <Talkie.h>

Talkie voice;

void setup() {
  Serial.begin(9600);
  voice.say("Hello, World!");
}

void loop() {
  // no es necesario implementar el loop() para que el altavoz diga el texto una sola vez
}
