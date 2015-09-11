#include <HX711.h>
#include <Adafruit_NeoPixel.h>

#define PIXEL_COUNT 100 //240
#define PIXEL_PIN 3

#define PIXEL_PIN_WEIGHT 7
#define PIXEL_COUNT_WEIGHT 11

#define PIXEL_PIN_BOTTOM 6
#define PIXEL_COUNT_BOTTOM 67

#define PIXEL_PIN_GLASS 5
#define PIXEL_COUNT_GLASS 15

#define PIXEL_PIN_ICE 4
#define PIXEL_COUNT_ICE 15

#define HX711_DOUT A1
#define HX711_PD_SCK A0

#define SCALE_CALIBRATION -418.76f

//predefined Colors
uint32_t c1;
uint32_t c2;
uint32_t c3;



//overall state in which we are
//0 = lights off, 1 = party mode, 2 = take bottle and pour, 3 = return bottle
int state = 42;
int current_pos = -1;
long last_weight = 0;
long desired_weight = 0;

long lastswitch = 0;
int frame = 0;

bool flag = false;

int posarray[17][3] = {
  { 7, 81 , 87  }
  ,
  { 8, 74, 79  }
  ,
  { 9, 66, 72  }
  ,
  { 10, 59, 64  }
  ,
  { 11, 52, 57  }
  ,
  { 12, 44, 50  }
  ,
  { 1, 0, 6  }
  ,
  { 2, 8, 13  }
  ,
  { 3, 15, 20  }
  ,
  { 4, 22, 28  }
  ,
  { 5, 30, 35  }
  ,
  { 6, 37, 43  }
  ,
  { 13, 61, 65  } // ICE 
  ,
  { 50, 71, 75  }
  ,
  { 60, 75, 80  }
  ,
  { 70, 81, 85  }
};

int weight_steady[] = {4, 5, 6};
int weight_circle[] = {0, 1, 2, 3, 10, 9, 8, 7};
int weight_frame = 0;
long weight_frame_time = 0;

long touch_time;
long touch_wait_time;
int touched = false;
boolean touched_flag = false;

boolean fill_finished = false;
long fill_finished_time = 0;

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
  colorAllPositions(strip.Color(127, 127, 127));
  stripWeight.begin();
  colorWeight(stripWeight.Color(127,127,127));
  stripBottom.begin();
  colorBottom(stripBottom.Color(127,127,127));
  stripGlass.begin();
  colorGlass(stripGlass.Color(127, 127, 127));
  stripIce.begin();
  colorIce(stripIce.Color(127,127,127));
  colorShaker(stripIce.Color(127,127,127));
  
  c1 = strip.Color(255, 0, 0);
  c2 = strip.Color(0, 255, 0);
  c3 = strip.Color(0, 0, 255);
  

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
        flag = false;
        current_pos = msg.substring(3, 6).toInt();
        desired_weight = msg.substring(6, 9).toInt();
        last_weight = scale.get_units(5);
        //Serial.println(msg);

      } 
      else if (state == 3) {
        frame = 0;
        flag = false;
        current_pos = msg.substring(3, 6).toInt();
        last_weight = scale.get_units(5);
        desired_weight = last_weight + msg.substring(6, 9).toInt();
        //Serial.println(msg);
      }
      
      else if (state == 10) {
        flag = false;
        last_weight = scale.get_units(5);
        desired_weight = last_weight + 10;
      }             

      else if (state == 11) {
        touched = false;
        last_weight = scale.get_units(5);
        desired_weight = last_weight + 10;
        touch_time = millis();
        touch_wait_time = msg.substring(3, 9).toInt();
        touched_flag = false;
      } 
      
      else if (state == 5 || state == 6) {
        last_weight = scale.get_units(5);
        desired_weight = last_weight + 10;
        flag = false;
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
    flag = false;
    break;
  case 2: // weight mode whole
  case 3: // weight mode add
  case 5: // take glass
  case 6: // take shaker
  case 10:// add ice
    {
      long current_weight = scale.get_units(1);
      if (current_weight < desired_weight) {
        fill_finished = false;
        colorEverything(strip.Color(0,255,0));
        if (state == 2 || state == 3) {
          colorPosition(current_pos);
        }
        else if (state == 5) {
          colorGlass(stripGlass.Color(0,0,255));
        }
        else if (state == 6) {
          colorShaker(stripIce.Color(0,0,255));
        }
        else if (state == 10) {
          colorIce(stripIce.Color(0,0,255));
        }
        long already_added = current_weight - last_weight;
        if (already_added < 0) already_added = 0;
        long needed = desired_weight - last_weight;
        int greenness = map(already_added, 0, needed, 0, 255);
        int redness = map(already_added, 0, needed, 255, 0);
        int fill_speed = map(already_added, 0, needed, 100, 0);
    
        colorWeightDuringFill(stripWeight.Color(redness, greenness, 0), fill_speed);      
        
      } else {
        
        colorAllPositions(strip.Color(0,255,0));
        colorWeight(stripWeight.Color(0, 255, 0));
        if (!fill_finished) {
          fill_finished = true;
          fill_finished_time = millis();
        } else if (millis() - fill_finished_time > 500) {
          if (!flag) {
            flag = true;
            Serial.println("READY");
          }
        }
      }
    }
    break;
    
  case 4: // return weight
    colorWeight(stripWeight.Color(127,127,127));
    flag = false;
    break;
    
  case 7: // fill shaker into glass
    colorWipe(strip.Color(45, 137, 239), 50); // Blue
    colorGlass(stripGlass.Color(45, 137, 239));
    colorWeight(stripWeight.Color(127,127,127));
    flag = false;
    break;
    
  case 8: // shake
    theaterChase(strip.Color(45, 137, 239), 25); // Blue
    colorWeight(stripWeight.Color(127,127,127));
    flag = false;
    break;
    
  case 9: // mix
    colorWipe(strip.Color(45, 137, 239), 50); // Blue
    flag = false;
    break;
    
 
  case 11: //Wait for touch
    {  
    long current_weight = scale.get_units(1);
      if (current_weight < desired_weight && !touched) {
        long already_waited = millis() - touch_time;
        if (already_waited < touch_wait_time) {
          int progress = map(already_waited, 0, touch_wait_time, 0, 100);
          int greenness = map(already_waited, 0, touch_wait_time, 255, 0);
          int redness = map(already_waited, 0, touch_wait_time, 0, 255);
          colorWeightDuringWait(stripWeight.Color(redness, greenness, 0), progress);
        } else {
          colorWeight(stripWeight.Color(255, 0, 0));
          if (!touched_flag) {
            touched_flag = true;
          Serial.println("NO_INPUT");
         }
        }
      }
      else if (current_weight > desired_weight || touched == true) {
        touched = true;
        colorWeight(stripWeight.Color(0, 255, 0));
         if (!touched_flag) {
          touched_flag = true;
          Serial.println("TOCUHED");
         }
      } 
    }
    break;    
  case 42:
    colorEverything(strip.Color(0,255,0));
    break;
  case 255:
    colorError();
    flag = false;
    break;
  default:
    colorError();
    colorWeight(stripWeight.Color(127,127,127));
    flag = false;
    break;
  }
  delay(50);
  strip.show();
  stripGlass.show();
  stripIce.show();
  stripBottom.show();
  stripWeight.show();
}

void colorAllPositions(uint32_t c) {
  for (uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);  
  }
  //strip.show();
}

void colorEverything(uint32_t c) {
  colorAllPositions(c);
  colorIce(c);
  colorShaker(c);
  colorGlass(c);
  colorBottom(c);
  colorWeight(c);
}


void colorWeight(uint32_t c) {
  for (uint16_t i=0; i<stripWeight.numPixels(); i++) {
    stripWeight.setPixelColor(i, c);  
  }
  //stripWeight.show();
}

void colorWeightDuringFill(uint32_t c, int fill_speed) {
  if (millis() - weight_frame_time > map(fill_speed, 0, 100, 500, 50)) {
    for (int i=0; i<sizeof(weight_steady)/sizeof(weight_steady[0]); i++) {
      stripWeight.setPixelColor(weight_steady[i], c);
    }
    for (int i=0; i<sizeof(weight_circle)/sizeof(weight_circle[0]); i++) {
      stripWeight.setPixelColor(weight_circle[i], 0);  
    }
    stripWeight.setPixelColor(weight_circle[weight_frame%(sizeof(weight_circle)/sizeof(weight_circle[0]))], c);
    stripWeight.setPixelColor(weight_circle[(weight_frame+1)%(sizeof(weight_circle)/sizeof(weight_circle[0]))], c);
    weight_frame_time = millis();
    weight_frame++;
  } 
}

void colorWeightDuringWait(uint32_t c, int progress) {
    for (int i=0; i<sizeof(weight_steady)/sizeof(weight_steady[0]); i++) {
      stripWeight.setPixelColor(weight_steady[i], c);
    }
    
    int length = sizeof(weight_circle)/sizeof(weight_circle[0]);
    int color_until = map(progress, 0, 100, length, 0);
    
    for (int i=0; i<sizeof(weight_circle)/sizeof(weight_circle[0]); i++) {
      if (i<color_until) {
        stripWeight.setPixelColor(weight_circle[i], c);
      } else {
        stripWeight.setPixelColor(weight_circle[i], 0);
      }  
    }

}

void colorBottom(uint32_t c) {
  for (uint16_t i=0; i<stripBottom.numPixels(); i++) {
    stripBottom.setPixelColor(i, c);  
  }
  //stripBottom.show();
}

void colorGlass(uint32_t c) {
  for (uint16_t i=0; i<stripGlass.numPixels(); i++) {
    stripGlass.setPixelColor(i, c);  
  }
  //stripGlass.show();
}

void colorIce(uint32_t c) {
  for (uint16_t i=0; i<7; i++) {
    stripIce.setPixelColor(i, c);  
  }
  //stripIce.show();
}
void colorShaker(uint32_t c) {
  for (uint16_t i=7; i<15; i++) {
    stripIce.setPixelColor(i, c);  
  }
  //stripIce.show();
}

void colorAllExceptPosition(uint32_t c, int pos) {
  int bounds[] = {0,0};
  getBounds(bounds, pos);
  //Serial.println(bounds[0]);
  //Serial.println(bounds[1]);
  for (uint16_t i=0; i<(bounds[0]); i++) {
    strip.setPixelColor(i, c);  
  }
  for (uint16_t i=(bounds[1]+1); i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);  
  }
  //strip.show();
}
void colorEverythingExceptPosition(uint32_t c, int pos) {
  colorAllExceptPosition(c, pos);
  colorGlass(c);
  colorBottom(c);
  colorWeight(c);
  colorShaker(c);
  colorIce(c);
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
   colorEverything(0);
}

void colorParty() {
  if (millis()-lastswitch > 250) {
    colorEverythingRandom();
    lastswitch = millis();
  }
}

void colorAllPositionsRandom() {
  for (int i=0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, strip.Color(random(127), random(255), random(255)));
  }
  //strip.show();
}

void colorBottomRandom() {
  for (int i=0; i < stripBottom.numPixels(); i++) {
    stripBottom.setPixelColor(i, strip.Color(random(127), random(255), random(255)));
  }
  //stripBottom.show();
}

void colorWeightRandom() {
  for (int i=0; i < stripWeight.numPixels(); i++) {
    stripWeight.setPixelColor(i, strip.Color(random(127), random(255), random(255)));
  }
  //stripWeight.show();
}

void colorIceRandom() {
  for (int i=0; i < stripIce.numPixels(); i++) {
    stripIce.setPixelColor(i, strip.Color(random(127), random(255), random(255)));
  }
  //stripIce.show();
}

void colorGlassRandom() {
  for (int i=0; i < stripGlass.numPixels(); i++) {
    stripGlass.setPixelColor(i, strip.Color(random(127), random(255), random(255)));
  }
  //stripGlass.show();
}

void colorEverythingRandom() {
  colorAllPositionsRandom();
  colorBottomRandom();
  colorWeightRandom();
  colorIceRandom();
  colorGlassRandom();
}

void colorPosition(int pos) {
  for (int i = 0; i < sizeof(posarray)/sizeof(posarray[0]); i++) {
    if (posarray[i][0] == pos) {
      for (int j = posarray[i][1]; j < posarray[i][2]+1; j++) {
        strip.setPixelColor(j, strip.Color(0, 0, 255));
      }

      //strip.show();
      //frame = ((frame) % (posarray[i][2]-posarray[i][1]))+1;

      break;
    }
  }
}

void colorError() {
  if (millis()-lastswitch > 250 && strip.getPixelColor(0) == 0) {
    colorEverything(strip.Color(255, 0, 0));
    lastswitch = millis();
  } 
  else if (millis()-lastswitch > 250) {
    colorEverything(0);
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


