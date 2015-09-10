#include "HX711.h"

// HX711.DOUT	- pin #A1
// HX711.PD_SCK	- pin #A0

HX711 scale(A1, A0);		// parameter "gain" is ommited; the default value 128 is used by the library
float known_weight = 265.0f;

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 Calibration");


  scale.set_scale();                  
  scale.tare();				    

  Serial.println("Place known weight (5s):");
  delay(5000);
  
  Serial.println("Measureing...");

  float value = scale.get_units(10);

  Serial.print("Value read average: \t\t");
  Serial.println(value);    
  
  float calibration = value/known_weight;

  Serial.print("Calibration value: \t\t");
  Serial.println(calibration);

  scale.set_scale(calibration);  
}

void loop() {
  Serial.print("one reading:\t");
  Serial.print(scale.get_units(), 1);
  Serial.print("\t| average:\t");
  Serial.println(scale.get_units(10), 1);
  delay(1000);
}
