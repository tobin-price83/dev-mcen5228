int bit1pin = 23;
int bit2pin = 25;
int bit3pin = 27;

int motor1 = 2;
int motor2 = 5;
int motor3 = 8;
int motor4 = 11;
int motor5 = 12;

void setup() {
  pinMode(bit1pin, INPUT);
  pinMode(bit2pin, INPUT);
  pinMode(bit3pin, INPUT);

  pinMode(motor1, OUTPUT);
  pinMode(motor2, OUTPUT);
  pinMode(motor3, OUTPUT);
  pinMode(motor4, OUTPUT);
  pinMode(motor5, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  bool a0 = digitalRead(bit1pin); // store bit1
  bool a1 = digitalRead(bit2pin); // store bit2
  bool a2 = digitalRead(bit3pin); // store bit3

  byte address = a0 + (a1 << 1) + (a2 << 2);

  // Assign motor states based on received value
  // NEED MOTOR PIN DEFS

  if (address = 0){
    digitalWrite(motor1, LOW);
    digitalWrite(motor2, LOW);
    digitalWrite(motor3, LOW);
    digitalWrite(motor4, LOW);
    digitalWrite(motor5, LOW);
  }
  
  if (address = 1) digitalWrite(motor1, HIGH);
  if (address = 2) digitalWrite(motor2, HIGH);
  if (address = 3) digitalWrite(motor3, HIGH);
  if (address = 4) digitalWrite(motor4, HIGH);
  if (address = 5) digitalWrite(motor5, HIGH);
  
  if (address = 6){
    digitalWrite(motor1, HIGH);
    digitalWrite(motor2, HIGH);
    digitalWrite(motor3, HIGH);
    digitalWrite(motor4, HIGH);
    digitalWrite(motor5, HIGH);
  }  
  
  
}
