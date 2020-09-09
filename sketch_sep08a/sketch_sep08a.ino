// Libraries declaration
#include <PneumaticStepper.h>
#include <ros.h>
#include <std_msgs/Float32MultiArray.h>

// Variables declaration
// Pin Base Motor
int m1p1   = 39;
int m1p2   = 41;
// Pin Mid Motor
int m2p1   = 43;
int m2p2   = 45;
// Pin Bot Motor
int m3p1   = 47;
int m3p2   = 49;
// Pin Top Motor
int m4p1   = 51;
int m4p2   = 53;

int mp[][2] = {{m1p1,m1p2},{m2p1,m2p2},{m3p1,m3p2},{m4p1,m4p2}};

int cylinder1=2;
int cylinder2=2;


//code added by me
int setMP[] = {0,0,0,0};
int setspeed = 10;

//old position value
int pos[] = {0, 0, 0, 0};
int phase[] = {0, 0, 0, 0};

bool flag_command = false;

PneumaticStepper stepper[] = {PneumaticStepper(2, true, false, 0, PneumaticStepper::ANY_ENGAGE, setspeed, pos[0], setMP[0], phase[0], true),
                              PneumaticStepper(2, true, false, 0, PneumaticStepper::ANY_ENGAGE, setspeed, pos[1], setMP[1], phase[1], true),
                              PneumaticStepper(2, true, false, 0, PneumaticStepper::ANY_ENGAGE, setspeed, pos[2], setMP[2], phase[2], true),
                              PneumaticStepper(2, true, false, 0, PneumaticStepper::ANY_ENGAGE, setspeed, pos[3], setMP[3], phase[3], true)};

//variable declaration of ros
ros::NodeHandle  nh;

std_msgs::Float32MultiArray pub_array;

ros::Publisher chatter("chatter", &pub_array);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  // pin output
  for (int i=0;i<4;i++){
    pinMode (mp[i][0],OUTPUT);
    pinMode (mp[i][1],OUTPUT);
    nh.initNode();
    nh.advertise(chatter);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  
  while(Serial.available()>0) {
    setMP[0] = Serial.parseInt();
    setMP[1] = Serial.parseInt();
    setMP[2] = Serial.parseInt();
    setMP[3] = Serial.parseInt();
    Serial.end();
    delay(100);
    Serial.begin(9600);
    
    for (int i=0;i<4;i++){
      stepper[i].setSetpoint(setMP[i]);
      // track all setPoint
      // Serial.print(mp[i][0]);
      // Serial.println(mp[i][1]);
    }
    // take a delay after receiving command from serial
    delay(2000);
    flag_command = true;
    Serial.println("New command received");
  }
  
  bool goal = true;
  
  if (goal && flag_command){
    Serial.println("in Goal");
    
    for (int i=0;i<4;i++){
      stepper[i].work();
    }
    
    // if set position and motor position are not the same
    if (flag_command){
      // All motor moves
      // Serial.println("Motors moving ...");
      for (int j=0;j<4;j++){
        cylinder1 = stepper[j].getCylinderState(0);
        cylinder2 = stepper[j].getCylinderState(1);
        cylinder1upd(cylinder1, mp[j][0]);
        cylinder2upd(cylinder2, mp[j][1]);
        delay(10);
      }
      
      // position and phase update
      Serial.println("Position and Phase updating ...");
      for (int j=0;j<4;j++){
        pos[j]   = stepper[j].getPosition();
        phase[j] = stepper[j].getPhaseNr();
      }      
      }

      pub_array.data=(float*)malloc(sizeof(float) * 4);
      pub_array.data_length= 4;

      for (int i=0; i<4; ++i){
          pub_array.data[i] = pos[i];
        }
      chatter.publish( &pub_array );

      // compare position and setpoint for all motor
      if (array_cmp(setMP, pos, 4, 4) == true){
        flag_command = false;
        goal = false;
      }
    
    }
  
  
}

void cylinder1upd(int state, int p1Pin){
 if (state==1){
  digitalWrite(p1Pin, HIGH);
  Serial.println(p1Pin);
  }
 else if(state==0){
  digitalWrite(p1Pin, LOW);
  }
  }

void cylinder2upd(int state, int p2Pin){
 if (state==1){
  digitalWrite(p2Pin, HIGH);
  Serial.println(p2Pin);
  }
 else if(state==0){
  digitalWrite(p2Pin, LOW);
  }
}

boolean array_cmp(int *a, int *b, int len_a, int len_b){
     int n;

     // if their lengths are different, return false
     if (len_a != len_b) return false;

     // test each element to be the same. if not, return false
     for (n=0;n<len_a;n++) if (a[n]!=b[n]) return false;

     //ok, if we have not returned yet, they are equal :)
     return true;
}
