#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>

#include <MeOrion.h>

MeBluetooth bluetooth(PORT_5);

double angle_rad = PI/180.0;
double angle_deg = 180.0/PI;
double ultrasonic_d;
double m1_speed;
double m2_speed;
double distance;
double speed;
MeUltrasonicSensor ultrasonic_3(3);
MeDCMotor motor_9(9);
MeDCMotor motor_10(10);

float learn_rate = 0.0001;

// Set some random weights
float weights[] = {0.01, 0.01};

int ARR_SIZE = 2;
int SPEED_LIMIT = 60;

float min_speed = -SPEED_LIMIT;


float Pred_Reward(float arr_x[]) {
  float total = 0.0;
  Serial.println();
  for(int i = 0; i < ARR_SIZE; i++) {
    total = total + (arr_x[i] * weights[i]);
    Serial.print("arr: ");
    Serial.print(arr_x[i]);
    Serial.println();
    Serial.print("weight: ");
    Serial.print(weights[i]);
    Serial.println();
  }
  Serial.println("---------");
  return total;
}

float Receive_Reward(float s) {
  float reward = 0.0;
  if(s>0.2 && s < 5) {
    reward = reward + 0.25;
  }
  else if(s>=5) {
    reward = reward + 1.0;
  }
  else if(s < 0.0) {
    reward = reward - 2.0;
  }
  else {
    reward = 0.0;
  }
  return reward;
}

void Update_Weights(float y_actual, float y_pred, float arr_x[])
{
  for(int i = 0; i < ARR_SIZE; i++) {
    float pDelta = (y_pred - y_actual) * arr_x[i];
    weights[i] = weights[i] - (learn_rate * pDelta);
  }
}

void setup(){
    Serial.begin(9600);

    bluetooth.begin(115200);    //The factory default baud rate is 115200
    m1_speed = random(-SPEED_LIMIT,(SPEED_LIMIT)+1);
    //m2_speed = random(-SPEED_LIMIT,(SPEED_LIMIT)+1);
    speed = 0;
}

void loop(){

    float arr_x[2] = {m1_speed, speed};

    float pred = Pred_Reward(arr_x);

//    Serial.println("Predicted Rewards:");
//    Serial.print(pred);
//    Serial.println();
    
    ultrasonic_d = ultrasonic_3.distanceCm();
    motor_9.run(m1_speed);
    motor_10.run(m1_speed);
    _delay(1);
    
    distance = (ultrasonic_d) - (ultrasonic_3.distanceCm());
    speed = (distance) / (1);

    Serial.print("Distance: ");
    Serial.print(distance, DEC);
    Serial.println();
    Serial.print("Speed is: ");
    Serial.print(speed, DEC);
    Serial.println();

    float a_reward;
    float y_reward;

    y_reward = pred;
    a_reward = Receive_Reward(speed);

    if(speed > 0 && pred > 0) {
      if(min_speed <= SPEED_LIMIT) {
        min_speed = min_speed + pred;
      }
    }

    m1_speed = random(min_speed, (SPEED_LIMIT)+1);
    if(m1_speed < 15 && m1_speed > 0) {
      m1_speed = 15;
    }
    if(m1_speed > -15 && m1_speed < 0) {
      m1_speed = -15;
    }
    //m2_speed = random((-SPEED_LIMIT+(weights[1]*100)), (SPEED_LIMIT)+1);

    Serial.println("-----------------------");
    Serial.print("MIN speed: ");
    Serial.print(min_speed);
    Serial.println();
    Serial.print("  Speed set: ");
    Serial.print(m1_speed);
    Serial.println();
    Serial.println(".....");
    Serial.print("Actual Reward: ");
    Serial.println(a_reward);
    Serial.print("Predicted Reward: ");
    Serial.print(y_reward);
    Serial.println(".....");

    Update_Weights(a_reward, y_reward, arr_x);
    
    _loop();
}

void _delay(float seconds){
    long endTime = millis() + seconds * 1000;
    while(millis() < endTime)_loop();
}

void _loop(){
    
}

