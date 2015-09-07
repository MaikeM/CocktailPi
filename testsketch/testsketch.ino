#include <Adafruit_NeoPixel.h>

#define PIXEL_COUNT 240
#define PIXEL_PIN 6

//overall state in which we are
//0 = lights off, 1 = party mode, 2 = take bottle and pour, 3 = return bottle
int state = 0;
int current_pos = -1;
int desired_weight = 0;

long lastswitch = 0;
int frame = 0;

int posarray[3][3] = {{1 ,2 ,7},
                 {2, 9, 14},
                 {3, 16, 21}};

Adafruit_NeoPixel strip = Adafruit_NeoPixel(PIXEL_COUNT, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600);
  strip.begin();
  colorAll(strip.Color(127, 127, 127));
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
    
    Serial.println(msg);
    Serial.println(msg.length());
    
    if (msg.length() ==  9) {
        
     String cmd = msg.substring(0, 3);
      
     state = cmd.toInt();
     
     if (state == 2) {
       frame = 0;
       current_pos = msg.substring(3, 6).toInt();
       desired_weight = msg.substring(6, 9).toInt();
       Serial.print("Position: ");
       Serial.println(msg.substring(3, 6));
       Serial.println(current_pos);
       Serial.print("Desired Weight: ");
       Serial.println(msg.substring(6, 9));
       Serial.println(desired_weight);
     }
     
    } else {
       Serial.println("ERROR");
    }
  }

  
  //change lights according to current state
  switch(state){
    case 0:
      colorOff();
      break;
    case 1:
      colorParty();
      break;
    case 2:
      colorAll(0);//(strip.Color(127,127,127));
      colorPosition(current_pos);
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
   } else if (millis()-lastswitch > 250) {
     colorAll(0);
     lastswitch = millis();
   }
}

