//Name: Kriston Rickman
//Date: 08/20/26
//V1.01
//Note: /*I made a mistake with creating my arduino
// code on hte python platform and transferring over*\

//Libraries
#include <Servo.h>

//variables
const byte navtrigpin = 1;
const byte 

//States
enum class State {
    off,
    search,
    center,
    LM1,
    LM2,
    LM3,
    NUM_STATES
};

//Events
enum class Event {
    btn_pushed,
    obstacle,
    LM1_found,
    LM2_found,
    LM3_found,
    NUM_EVENTS
};

//The total number of states and events
const int NUM_STATES = static_cast<int>(State::NUM_STATES);
const int NUM_EVENTS = static_cast<int>(Event::NUM_EVENTS);

//Transition table
State transitionTable[NUM_STATES][NUM_EVENTS] = {
    //btn_push,       Obstacles,         LM1_found        LM2_found,       LM3_found
    {State::center,  State::center,      State::off,      State::off,      State::off },  // off
    {State::off,     State::center,      State::LM1,      State::LM2,      State::LM3 },  // search
    {State::off,     State::center,      State::LM1,      State::LM2,      State::LM3 },  // center
    {State::off,     State::center,      State::LM1,      State::LM2,      State::LM3 },  // LM1
    {State::off,     State::center,      State::LM1,      State::LM2,      State::LM3 },  // LM2
    {State::off,     State::center,      State::LM1,      State::LM2,      State::LM3 }   // LM3
};


void setup() {
  Serial.begin(11520);

}

void loop() {
  

}


void turnON()
{
  Serial.println("Push the button to start...");
  if (btn_state==0)
  {
    while (btn_state==0){}
    currentState = State::center;
  }
}



//This code is based off Tin's functions and will work when integrating all code together
// Turn robot left
void turnLeft()
{
  rightmotor(150);
  leftmotor(-150);
}

// Turn robot right
void turnRight()
{
  rightmotor(-150);
  leftmotor(150);
}

// Stop both motors
void stopMotor()
{
  rightmotor(0);
  leftmotor(0);
}



void search()
{
    // Robot moves forward while searching
    rightmotor(150);
    leftmotor(150);

    // Check for obstacle
    if (distance < 30)
    {
        stopMotor();
        currentState = State::center;
        return;
    }

    // Check for landmark information from Raspberry Pi
    if (Serial.available())
    {
        String message = Serial.readStringUntil('\n');

        if (message == "LM1")
        {
            stopMotor();
            currentState = State::LM1;
        }
        else if (message == "LM2")
        {
            stopMotor();
            currentState = State::LM2;
        }
        else if (message == "LM3")
        {
            stopMotor();
            currentState = State::LM3;
        }
    }
}



void centerOnLandmark()
{
    int cameraAngle = targetServoAngle;

    // Landmark is to the LEFT of robot
    if (cameraAngle < 90)
    {
        turnLeft();

        // Keep camera pointed at landmark
        cameraAngle += 2;
        cameraServo.write(cameraAngle);
    }

    // Landmark is to the RIGHT of robot
    else if (cameraAngle > 90)
    {
        turnRight();

        // Keep camera pointed at landmark
        cameraAngle -= 2;
        cameraServo.write(cameraAngle);
    }

    // Landmark is directly ahead
    else
    {
        stopMotors();
        currentState = State::search;
    }
}
