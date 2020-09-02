// Libraries declaration

#include <ros.h>
#include <std_msgs/UInt16.h>

#include <PneumaticStepper.h>

// Variables declaration of motor 
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

//coupling the pins in an 2D array
int mp[][2] = {{m1p1,m1p2},{m2p1,m2p2},{m3p1,m3p2},{m4p1,m4p2}};

//cylinder ???
int cylinder1=2;
int cylinder2=2;

//an array that carries the new setpoints
//code added by me
int setMP[] = {0,0,0,0};
//variable that carries a fixed speed
int setspeed = 10;

//old position value
int pos[] = {0, 0, 0, 0};
//old phase value ??
int phase[] = {0, 0, 0, 0};

//boolean used for ?? 
bool flag_command = false;
bool drop = false;

//creating the motor object array with multiple different steppers
//(nr of cylnders, if its double acting, if its tristate, approach direction, cylinderStrategy, frequency/speed, position, setpoint, phasenr, running)
//double acting: if it has two rows of teeth phased 180 deg apart
//0 means it does not matter what approach direction 
//

PneumaticStepper stepper[] = {PneumaticStepper(2, true, false, 0, PneumaticStepper::ANY_ENGAGE, setspeed, pos[0], setMP[0], phase[0], true),
                              PneumaticStepper(2, true, false, 0, PneumaticStepper::ANY_ENGAGE, setspeed, pos[1], setMP[1], phase[1], true),
                              PneumaticStepper(2, true, false, 0, PneumaticStepper::ANY_ENGAGE, setspeed, pos[2], setMP[2], phase[2], true),
                              PneumaticStepper(2, true, false, 0, PneumaticStepper::ANY_ENGAGE, setspeed, pos[3], setMP[3], phase[3], true)};

//variable declaration of ros
ros::NodeHandle  nh;

//callback 
void servo_cb( const std_msgs::UInt16& cmd_msg){
 //here is where the updating is done
 //for now we keep the other setpoints zero
 if (cmd_msg.data==2){
    setMP[0] = -340;
    nh.loginfo("");
    }
 else if (cmd_msg.data==1){
    int position1=0;
    int setpoint1=0;
    String str;
    String str2;
    char b[4];
    char a[4];
    
    position1=stepper[0].getPosition();
    setpoint1=stepper[0].getSetpoint();
    
    str=String(position1);
    str.toCharArray(b,4);

    str2=String(setpoint1);
    str2.toCharArray(a,4);
    
    nh.loginfo(b);
    nh.loginfo(a);

    //stepper[0].setSetpoint(0);
    setMP[0] = 0;
    stepper[0].setPosition(0);

    str=String(position1);
    str.toCharArray(b,4);

    str2=String(setpoint1);
    str2.toCharArray(a,4);
    
    nh.loginfo(b);
    nh.loginfo(a);
    
    drop = false;
    
    }
    
 else if (cmd_msg.data==0){
    setMP[0] = 0;
    nh.loginfo("0");
  }
  else{
    }
    setMP[1] = 0;
    setMP[2] = 0;
    setMP[3] = 0;

    //set the setpoint
    for (int i=0;i<4;i++){
      stepper[i].setSetpoint(setMP[i]);
    }
    
    flag_command = true;
    //Serial.println("New command received");

    bool goal = true;
    drop = true;

    if (goal && flag_command){
    //Serial.println("in Goal");

    //start updating the state of the motor with the work function 
    for (int i=0;i<4;i++){
      stepper[i].work();
    }
    
    // if set position and motor position are not the same
    if (flag_command){
      // All motor are moved // how does this change from the work function ?
      // Serial.println("Motors moving ...");

      //for all the motors get the cylinder states 1 and 2 
      //update the cylinders with the values from the array 
      for (int j=0;j<4;j++){
        cylinder1 = stepper[j].getCylinderState(0);
        cylinder2 = stepper[j].getCylinderState(1);
        
        //function that updates the cylinders 
        cylinder1upd(cylinder1, mp[j][0]);
        cylinder2upd(cylinder2, mp[j][1]);
        delay(10);
      }
      
      // position and phase update
      //Serial.println("Position and Phase updating ...");
      for (int j=0;j<4;j++){
        //updating the position and phase arrays
        pos[j]   = stepper[j].getPosition();
        phase[j] = stepper[j].getPhaseNr();
      }
      
      }

      // compare position and setpoint for all motor
      // if the values are the same return flag_command as false
      // and goal as false
      // if they are not the same keep updating the motor
      if (array_cmp(setMP, pos, 4, 4) == true){
        flag_command = false;
        goal = false;
        //Serial.println("The end");
      }
    
    }
 
}

ros::Subscriber<std_msgs::UInt16> sub("servo", servo_cb);

void setup() {
  // put your setup code here, to run once:
    // put your setup code here, to run once:
  //Serial.begin(57600);

  //set all the pins for the motors as output this is the actual physical voltage
  // pin output
  for (int i=0;i<4;i++){
    pinMode (mp[i][0],OUTPUT);
    pinMode (mp[i][1],OUTPUT);
    nh.initNode();
    nh.subscribe(sub);
  }
  

}

void loop() {
  // put your main code here, to run repeatedly:
  nh.spinOnce();
  delay(1);
}

//functions of the motor
void cylinder1upd(int state, int p1Pin){
 if (state==1){
  digitalWrite(p1Pin, HIGH);
  //Serial.println(p1Pin);
  }
 else if(state==0){
  digitalWrite(p1Pin, LOW);
  }
  }

void cylinder2upd(int state, int p2Pin){
 if (state==1){
  digitalWrite(p2Pin, HIGH);
  //Serial.println(p2Pin);
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
