#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); // Dirección I2C y tamaño de la pantalla

void setup() {
  lcd.init(); // Inicializar la pantalla LCD
  lcd.backlight(); // Encender la luz de fondo
}

void loop() {
  lcd.clear(); // Limpiar la pantalla

  // Imprimir un mensaje en la primera línea de la pantalla
  lcd.setCursor(0, 0);
  lcd.print("Hola mundo!");

  // Imprimir un mensaje en la segunda línea de la pantalla
  lcd.setCursor(0, 1);
  lcd.print("Desde Arduino");

  // Agregar aquí cualquier otro código que deseas ejecutar en el loop()
}
