/*
   Make an RGB LED smoothly change between colors using PWM.  Implemented on NodeMCU.

   Glenn K. Lockwood
*/
#define VERBOSE 0
int pin[3]; /* pins for red, green, and blue */
int brightness[3]; /* state of each pin's PWM */
int bright_max = 255;
int fade_amount = 5;

void setup() {
  for ( int i = 0; i < 3; i++ ) {
    pinMode(i, OUTPUT);
  }

  pin[0] = D1;
  pin[1] = D2;
  pin[2] = D3;
  brightness[0] = 0;
  brightness[1] = 0;
  brightness[2] = 0;

#if VERBOSE != 0
  Serial.begin(115200);
#endif
}

void loop() {
  int iters = bright_max / fade_amount + 1;
  int incr = fade_amount;
  long r = random(3);

  /* cycle the LED from 0 to bright_max or vice versa */
  for (int i = 0; i < iters; i++) {

    analogWrite(pin[r], brightness[r]);

    /* keep the brightness bouncing between 0 and bright_max */
    brightness[r] = brightness[r] + incr;
    if (brightness[r] <= 0 || brightness[r] >= bright_max) {
      incr = -incr;
    }
    brightness[r] = max(brightness[r], 0);
    brightness[r] = min(brightness[r], bright_max);

#if VERBOSE != 0
    /* print pwm state for each pin to serial output */
    Serial.print( brightness[0] );
    Serial.print( " " );
    Serial.print( brightness[1] );
    Serial.print( " " );
    Serial.println( brightness[2] );
#endif

    delay(30);
  }
}
