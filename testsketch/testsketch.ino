#include <HX711.h>
#include <Adafruit_NeoPixel.h>

#define PIXEL_COUNT 100 //240
#define PIXEL_PIN 6
#define PIXEL_PIN_WEIGHT 7
#define PIXEL_COUNT_WEIGHT 11
#define PIXEL_PIN_BOTTOM 5
#define PIXEL_COUNT_BOTTOM 67
#define PIXEL_PIN_GLASS 4
#define PIXEL_COUNT_GLASS 11
#define PIXEL_PIN_ICE 7
#define PIXEL_COUNT_ICE 20

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

bool flag = false;

int posarray[17][3] = {
  { 1, 81 , 87  }
  ,
  { 2, 74, 79  }
  ,
  { 3, 66, 72  }
  ,
  { 4, 59, 64  }
  ,
  { 5, 52, 57  }
  ,
  { 6, 44, 50  }
  ,
  { 7, 0, 6  }
  ,
  { 8, 8, 13  }
  ,
  { 9, 15, 20  }
  ,
  { 10, 22, 28  }
  ,
  { 11, 30, 35  }
  ,
  { 12, 37, 43  }
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
Adafruit_NeoPixel stripWeight = Adafruit_NeoPixel(PIXEL_COUNT_WEIGHT, PIXEL_PIN_WEIGHT, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel stripBottom = Adafruit_NeoPixel(PIXEL_COUNT_BOTTOM, PIXEL_PIN_BOTTOM, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel stripGlass = Adafruit_NeoPixel(PIXEL_COUNT_GLASS, PIXEL_PIN_GLASS, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel stripIce = Adafruit_NeoPixel(PIXEL_COUNT_ICE, PIXEL_PIN_ICE, NEO_GRB + NEO_KHZ800);

void setup() {
  //Initialize serial connection
  Serial.begin(9600);

  //Initialize NeoPixels
  strip.begin();
  colorAll(strip.Color(127, 127, 127));
  stripWeight.begin();
  colorWeight(stripWeight.Color(127,127,127));
  stripBottom.begin();
  colorBottom(stripBottom.Color(127,127,127));
  stripGlass.begin();
  colorGlass(stripGlass.Color(127,127,127));
  stripIce.begin();
  colorIce(stripIce.Color(127,127,127));
  

  //Initialize scale
  scale.set_scale(SCALE_CALIBRATION);                      // this value is obtained by calibrating the scale with known weights
  scale.tare();				        // reset the scale to 0

  //Wait briefly, so we can see the startup/reset
  delay(1000);  
}

void loop() {
  //receive command via serial and change state accordingly
  String msg = "";
  bool msg_send = false;
  if (Serial.available() > 0) {
    while (Serial.available()) {
      char c = Serial.read();  //gets one byte from serial buffer
      msg += c; //makes the String readString
      delay(5);  //slow looping to allow buffer to fill with next character
    }
    
    if (msg.length() ==  9) {

      String cmd = msg.substring(0, 3);

      state = cmd.toInt();

      if (state == 2) {
        frame = 0;
        current_pos = msg.substring(3, 6).toInt();
        desired_weight = msg.substring(6, 9).toInt();
        //Serial.println(msg);

      } 
      else if (state == 3) {
        frame = 0;
        current_pos = msg.substring(3, 6).toInt();
        long current_weight = scale.get_units(5);
        desired_weight = current_weight + msg.substring(6, 9).toInt();
        //Serial.println(msg);
      } 
      else if(state == 4) {
        //Serial.println(scale.get_units(2), 1);
        state = msg.substring(3, 6).toInt();
      } 
      else {
        //Serial.println(msg);
      }


    } 
    else {
      //Serial.println("ERROR");
      msg= "ERROR";
    }
  }

  if (!msg_send && msg != ""){
    msg_send = true;
    Serial.println(msg);
  }

  
  //change lights according to current state
  switch(state){
  case 0: // off
    colorOff();
    flag = false;
    break;
  case 1: // party
    colorParty();
    colorWeight(stripWeight.Color(127,127,127));
    flag = false;
    break;
  case 2: // licht1
  case 3: { // licht 2
    long current_weight = scale.get_units(2);
    if (current_weight < desired_weight) {
      colorAllExceptPosition(strip.Color(127,127,127), current_pos);
      colorPosition(current_pos);
      flag = false;
      if (current_weight < (desired_weight*0.1f)){
        colorWeight(stripWeight.Color(255,0,0));
      } else if (current_weight < (desired_weight*0.2f)){
        colorWeight(stripWeight.Color(205,38,38));
      } else if (current_weight < (desired_weight*0.4f)){
        colorWeight(stripWeight.Color(255,140,0));
      } else if (current_weight < (desired_weight*0.6f)){
        colorWeight(stripWeight.Color(255,215,0));
      } else if (current_weight < (desired_weight*0.8f)){
        colorWeight(stripWeight.Color(255,255,0));
      } else {
        colorWeight(stripWeight.Color(205,205,0));
        }
        
    } else {
      colorAll(strip.Color(127,127,127));
      colorWeight(stripWeight.Color(127,255,0));
      if (!flag) {flag = true;
      Serial.println("READY");}
    }}
    break;
  case 4: // waage
    colorAllExceptPosition(strip.Color(127,127,127), 50);
    colorPosition(50);
    colorWeight(stripWeight.Color(127,127,127));
    flag = false;
    break;
  case 5: // take glass
    colorAllExceptPosition(strip.Color(127,127,127), 60);
    colorPosition(60);
    colorWeight(stripWeight.Color(127,127,127));
    flag = false;
    break;
  case 6: // take shaker
    colorAllExceptPosition(strip.Color(127,127,127), 70);
    colorPosition(70);
    colorWeight(stripWeight.Color(127,127,127));
    flag = false;
    break;
  case 7: // fill shaker into glass
    theaterChase(strip.Color(45, 137, 239), 50); // Blue
    colorWeight(stripWeight.Color(127,127,127));
    flag = false;
    break;
  case 8: // shake
    colorWipe(strip.Color(45, 137, 239), 25); // Blue
    colorWeight(stripWeight.Color(127,127,127));
    flag = false;
    break;
  case 9: // mix
    colorWipe(strip.Color(45, 137, 239), 50); // Blue
    colorWeight(stripWeight.Color(127,127,127));
    flag = false;
    break;
  case 255:
    colorError();
    colorWeight(stripWeight.Color(127,127,127));
    flag = false;
    break;
  default:
    colorError();
    colorWeight(stripWeight.Color(127,127,127));
    flag = false;
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

void colorWeight(uint32_t c) {
  for (uint16_t i=0; i<stripWeight.numPixels(); i++) {
    stripWeight.setPixelColor(i, c);  
  }
  stripWeight.show();
}

void colorBottom(uint32_t c) {
  for (uint16_t i=0; i<stripBottom.numPixels(); i++) {
    stripBottom.setPixelColor(i, c);  
  }
  stripBottom.show();
}

void colorGlass(uint32_t c) {
  for (uint16_t i=0; i<stripGlass.numPixels(); i++) {
    stripGlass.setPixelColor(i, c);  
  }
  stripGlass.show();
}

void colorIce(uint32_t c) {
  for (uint16_t i=0; i<stripIce.numPixels(); i++) {
    stripIce.setPixelColor(i, c);  
  }
  stripIce.show();
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


