int ledPin = 13;
void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}
void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'F') {
      digitalWrite(ledPin, HIGH);
    }
    else if (command == 'O') {
      digitalWrite(ledPin, LOW);
    }
  }
}
