/* --- region tests --- */
#define TEST_LED        1
#define TEST_SERVO      1
/* --- endregion tests --- */


/* --- region defines --- */
#define LED_PIN 8
/* --- endregion defines --- */


/* --- region setup --- */
// the setup function runs once when you press reset or power the board
void setup() {
    // initialize digital pin LED_BUILTIN as an output.
#ifdef TEST_LED
    pinMode(LED_PIN, OUTPUT);
#endif /* TEST_LED */
}
/* --- endregion setup --- */


/* --- region loop --- */
// the loop function runs over and over again forever
void loop() {
#ifdef TEST_LED
    digitalWrite(LED_PIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(2000);                       // wait for a second
    digitalWrite(LED_PIN, LOW);    // turn the LED off by making the voltage LOW
    delay(2000);                       // wait for a second
#endif /* TEST_LED */

}
/* --- endregion loop --- */
