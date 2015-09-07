#include <HX711.h>
#include <Adafruit_NeoPixel.h>

#define PIXEL_COUNT 100 //240
#define PIXEL_PIN 6

#define HX711_DOUT A1
#define HX711_PD_SCK A0

#define SCALE_CALIBRATION -408.50f

//overall state in which we are
//0 = lights off, 1 = party mode, 2 = take bottle and pour, 3 = return bottle
int state = 0;
int current_pos = -1;
long desired_weight = 0;

long lastswitch = 0;
int frame = 0;

int posarray[17][3] = {
  { 1 ,1 ,5  }
  ,
  { 2, 6, 10  }
  ,
  { 3, 11, 15  }
  ,
  { 4, 16, 20  }
  ,
  { 5, 21, 25  }
  ,
  { 6, 26, 30  }
  ,
  { 7, 31, 35  }
  ,
  { 8, 36, 40  }
  ,
  { 9, 41, 45  }
  ,
  { 10, 46, 50  }
  ,
  { 11, 51, 55  }
  ,
  { 12, 56, 60  }
  ,
  { 13, 61, 65  } // ICE 
  ,
  { 50, 71, 75  }
  ,
  { 60, 75, 80  }
  ,
  { 70, 81, 85  }
};

HX711 scale(HX711_DOUT, HX711_PD_SCK);		// parameter "gain" is ommited; the default value 128 is used by the library

Adafruit_NeoPixel strip = Adafruit_NeoPixel(PIXEL_COUNT, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  //Initialize serial connection
  Serial.begin(9600);

  //Initialize NeoPixels
  strip.begin();
  colorAll(strip.Color(127, 127, 127));

  //Initialize scale
  scale.set_scale(SCALE_CALIBRATION);                      // this value is obtained by calibrating the scale with known weights
  scale.tare();				        // reset the scale to 0

  //Wait briefly, so we can see the startup/reset
  delay(1000);  
}

void loop() {
  //receive command via serial and change state accordingly
  String msg = "";
  if (Serial.available() > 0) {
    while (Serial.available()) {
      char c = Serial.read();  //gets one byte from serial buffer
      msg += c; //makes the String readString
      delay(5);  //slow looping to allow buffer to fill with next character
    }

    //Serial.println(msg);
    //Serial.println(msg.length());

    if (msg.length() ==  9) {

      String cmd = msg.substring(0, 3);

      state = cmd.toInt();

      if (state == 2) {
        frame = 0;
        current_pos = msg.substring(3, 6).toInt();
        desired_weight = msg.substring(6, 9).toInt();
        Serial.println(msg);

      } 
      else if (state == 3) {
        frame = 0;
        current_pos = msg.substring(3, 6).toInt();
        long current_weight = scale.get_units(5);
        desired_weight = current_weight + msg.substring(6, 9).toInt();
        Serial.println(msg);

      } 
      else if(state == 4) {
        Serial.println(scale.get_units(2), 1);
        state = current_pos = msg.substring(3, 6).toInt();
      } 
      else {
        Serial.println(msg);
      }


    } 
    else {
      Serial.println("ERROR");
    }
  }


  //change lights according to current state
  switch(state){
  case 0: // off
    colorOff();
    break;
  case 1: // party
    colorParty();
    break;
  case 2: // licht1
  case 3: // licht 2
    colorAllExceptPosition(strip.Color(127,127,127), current_pos);
    colorPosition(current_pos);
    break;
  case 4: // waage
    colorAllExceptPosition(strip.Color(127,127,127), 50);
    colorPosition(50);
    break;
  case 5: // take glass
    colorAllExceptPosition(strip.Color(127,127,127), 60);
    colorPosition(60);
    break;
  case 6: // take shaker
    colorAllExceptPosition(strip.Color(127,127,127), 70);
    colorPosition(70);
    break;
  case 7: // fill shaker into glass
    theaterChase(strip.Color(45, 137, 239), 50); // Blue
    break;
  case 8: // shake
    colorWipe(strip.Color(45, 137, 239), 25); // Blue
    break;
  case 9: // mix
    colorWipe(strip.Color(45, 137, 239), 50); // Blue
    break;
  case 255:
    colorError();
    break;
  default:
    colorError();
    break;
  }

  delay(250);
}

void colorAll(uint32_t c) {
  for (uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);  
  }
  strip.show();
}

void colorAllExceptPosition(uint32_t c, int pos) {
  int bounds[] = {0,0};
  getBounds(bounds, pos);
  //Serial.println(bounds[0]);
  //Serial.println(bounds[1]);
  for (uint16_t i=0; i<(bounds[0]); i++) {
    strip.setPixelColor(i, c);  
  }
  for (uint16_t i=(bounds[1]); i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);  
  }
  strip.show();
}


// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}
//Theatre-style crawling lights.
void theaterChase(uint32_t c, uint8_t wait) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (int i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, c);    //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (int i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}
void colorOff() {
   colorAll(0);
}

void colorParty() {
  if (millis()-lastswitch > 250) {
    colorAllRandom();
    lastswitch = millis();
  }
}

void colorAllRandom() {
  for (int i=0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, strip.Color(random(127), random(255), random(255)));
  }
  strip.show();
}

void colorPosition(int pos) {
  for (int i = 0; i < sizeof(posarray)/sizeof(posarray[0]); i++) {
    if (posarray[i][0] == pos) {
      for (int j = posarray[i][1]; j < posarray[i][2]+1; j++) {
        /*if (frame == posarray[i][2] -j) {
         strip.setPixelColor(j, strip.Color(255, 255, 0));
         } else {
         strip.setPixelColor(j, strip.Color(0, 127, 127));
         }*/
        strip.setPixelColor(j, strip.Color(45, 137, 239));
      }

      strip.show();
      //frame = ((frame) % (posarray[i][2]-posarray[i][1]))+1;

      break;
    }
  }
}

void colorError() {
  if (millis()-lastswitch > 250 && strip.getPixelColor(0) == 0) {
    colorAll(strip.Color(255, 0, 0));
    lastswitch = millis();
  } 
  else if (millis()-lastswitch > 250) {
    colorAll(0);
    lastswitch = millis();
  }
}

void getBounds(int return_array[], int pos) {
  for (int i = 0; i < sizeof(posarray)/sizeof(posarray[0]); i++) {
    if (posarray[i][0] == pos) {
      return_array[0] = posarray[i][1];
      return_array[1] = posarray[i][2];
    }
  }
} 


