/*NASA SpaceApps 2016
 Mars UPV Team
 Code for Arduino MEGA 2560 and a bluetooth serial bridge.
 IMU code from Pololu's MiniIMU-9-Arduino-AHRS
 Shared under GNU GPL 3 http://www.gnu.org/licenses/gpl-3.0.en.html
*/
int SENSOR_SIGN[9] = {1, 1, 1, -1, -1, -1, 1, 1, 1}; //Correct directions x,y,z - gyro, accelerometer, magnetometer

#include <Wire.h>
#include <Servo.h>

// LSM303 accelerometer: 8 g sensitivity
// 3.9 mg/digit; 1 g = 256
#define GRAVITY 256  //this equivalent to 1G in the raw data coming from the accelerometer

#define ToRad(x) ((x)*0.01745329252)  // *pi/180
#define ToDeg(x) ((x)*57.2957795131)  // *180/pi

// L3G4200D gyro: 2000 dps full scale
// 70 mdps/digit; 1 dps = 0.07
#define Gyro_Gain_X 0.07 //X axis Gyro gain
#define Gyro_Gain_Y 0.07 //Y axis Gyro gain
#define Gyro_Gain_Z 0.07 //Z axis Gyro gain
#define Gyro_Scaled_X(x) ((x)*ToRad(Gyro_Gain_X)) //Return the scaled ADC raw data of the gyro in radians for second
#define Gyro_Scaled_Y(x) ((x)*ToRad(Gyro_Gain_Y)) //Return the scaled ADC raw data of the gyro in radians for second
#define Gyro_Scaled_Z(x) ((x)*ToRad(Gyro_Gain_Z)) //Return the scaled ADC raw data of the gyro in radians for second

// LSM303 magnetometer calibration constants; use the Calibrate example from
// the Pololu LSM303 library to find the right values for your board
#define M_X_MIN -421
#define M_Y_MIN -639
#define M_Z_MIN -238
#define M_X_MAX 424
#define M_Y_MAX 295
#define M_Z_MAX 472

#define Kp_ROLLPITCH 0.02
#define Ki_ROLLPITCH 0.00002
#define Kp_YAW 1.2
#define Ki_YAW 0.00002

/*For debugging purposes*/
//OUTPUTMODE=1 will print the corrected data,
//OUTPUTMODE=0 will print uncorrected data of the gyros (with drift)
#define OUTPUTMODE 1

//#define PRINT_DCM 0     //Will print the whole direction cosine matrix
#define PRINT_ANALOGS 0 //Will print the analog raw data
#define PRINT_EULER 0   //Will print the Euler angles Roll, Pitch and Yaw

#define STATUS_LED 50

float G_Dt = 0.02;  // Integration time (DCM algorithm)  We will run the integration loop at 50Hz if possible

long timer = 0; //general purpuse timer
long timer_old;
long timer24 = 0; //Second timer used to print values
int AN[6]; //array that stores the gyro and accelerometer data
int AN_OFFSET[6] = {0, 0, 0, 0, 0, 0}; //Array that stores the Offset of the sensors

int gyro_x;
int gyro_y;
int gyro_z;
int accel_x;
int accel_y;
int accel_z;
int magnetom_x;
int magnetom_y;
int magnetom_z;
float c_magnetom_x;
float c_magnetom_y;
float c_magnetom_z;
float MAG_Heading;

float Accel_Vector[3] = {0, 0, 0}; //Store the acceleration in a vector
float Gyro_Vector[3] = {0, 0, 0}; //Store the gyros turn rate in a vector
float Omega_Vector[3] = {0, 0, 0}; //Corrected Gyro_Vector data
float Omega_P[3] = {0, 0, 0}; //Omega Proportional correction
float Omega_I[3] = {0, 0, 0}; //Omega Integrator
float Omega[3] = {0, 0, 0};

// Euler angles
float roll;
float pitch;
float yaw;

float errorRollPitch[3] = {0, 0, 0};
float errorYaw[3] = {0, 0, 0};

unsigned int counter = 0;
byte gyro_sat = 0;

float DCM_Matrix[3][3] = {
  {
    1, 0, 0
  }
  , {
    0, 1, 0
  }
  , {
    0, 0, 1
  }
};
float Update_Matrix[3][3] = {{0, 1, 2}, {3, 4, 5}, {6, 7, 8}}; //Gyros here


float Temporary_Matrix[3][3] = {
  {
    0, 0, 0
  }
  , {
    0, 0, 0
  }
  , {
    0, 0, 0
  }
};

//Voltímetro
#define pin_Voltaje_1 A0
#define pin_Voltaje_2 A1
#define pin_Voltaje_3 A2

//LDR
#define pin_LDR_1 A3
#define pin_LDR_2 A4
#define pin_LDR_3 A5
#define pin_LDR_4 A6

//Termistores
#define pin_termistor_1 A8
#define pin_termistor_2 A9

//Servos
#define pin_servo_1 22
#define pin_servo_2 24
#define pin_servo_3 26
#define pin_servo_4 28
#define pin_servo_5 30
#define pin_servo_6 32

//Leds
#define pin_led_1   2 //LEDS Traje
#define pin_led_2   3 //LEDs tobera R
#define pin_led_3   4 //LEDs tobera G
#define pin_led_4   5 //LEDs tobera B
#define pin_led_5   6
#define pin_led_6   7
#define pin_led_7   8
#define pin_led_8   9
#define pin_led_9   10
#define pin_led_10  11
#define pin_led_11  12
#define pin_led_12  13

//Jostick
#define pin_Jostick1_X A10
#define pin_Jostick1_Y A11
#define pin_Jostick2_X A13
#define pin_Jostick2_Y A14
#define pin_Pulsador_Jostick1 A12 //(digital INPUT_PULLUP)
#define pin_Pulsador_Jostick2 A15
#define send_bluetooth true
#define send_servos true
#define send_bluetooth_serialUSB false
#define test_bluetooth false
bool leds_encendidos=false;

Servo servo1, servo2, servo3, servo4, servo5, servo6;

void setup()
{
  Serial.begin(115200);
  Serial1.begin(38400);
  pinMode (STATUS_LED, OUTPUT); // Status LED

  pinMode(pin_led_1, OUTPUT);
  pinMode(pin_led_2, OUTPUT);
  pinMode(pin_led_3, OUTPUT);
  pinMode(pin_led_4, OUTPUT);
  pinMode(pin_led_5, OUTPUT);
  pinMode(pin_led_6, OUTPUT);
  pinMode(pin_led_7, OUTPUT);
  pinMode(pin_led_8, OUTPUT);
  pinMode(pin_led_9, OUTPUT);
  pinMode(pin_led_10, OUTPUT);
  pinMode(pin_led_11, OUTPUT);
  pinMode(pin_led_12, OUTPUT);
  pinMode(pin_Pulsador_Jostick1, INPUT_PULLUP);
  pinMode(pin_Pulsador_Jostick2, INPUT_PULLUP);
  servo1.attach(pin_servo_1);
  servo2.attach(pin_servo_2);
  servo3.attach(pin_servo_3);
  servo4.attach(pin_servo_4);
  servo5.attach(pin_servo_5);
  servo6.attach(pin_servo_6);
  servo1.write(90);
  servo2.write(90);
  servo3.write(90);
  servo4.write(90);
  servo5.write(90);
  servo6.write(90);

  I2C_Init();

  digitalWrite(STATUS_LED, LOW);
  delay(10000);

  Accel_Init();
  Compass_Init();
  Gyro_Init();
  Serial.println("Inicializacion completa, calibrando...");
  delay(20);

  for (int i = 0; i < 32; i++) // We take some readings...
  {
    Read_Gyro();
    Read_Accel();
    for (int y = 0; y < 6; y++) // Cumulate values
      AN_OFFSET[y] += AN[y];
    delay(20);
  }

  for (int y = 0; y < 6; y++)
    AN_OFFSET[y] = AN_OFFSET[y] / 32;

  AN_OFFSET[5] -= GRAVITY * SENSOR_SIGN[5];

  //Serial.println("Offset:");
  for (int y = 0; y < 6; y++)
    Serial.println(AN_OFFSET[y]);

  delay(2000);
  digitalWrite(STATUS_LED, HIGH);

  timer = millis();
  delay(20);
  counter = 0;
}

void loop() //Main Loop
{
  if ((millis() - timer) >= 20) // Main loop runs at 50Hz
  {
    counter++;
    timer_old = timer;
    timer = millis();
    if (timer > timer_old)
      G_Dt = (timer - timer_old) / 1000.0; // Real time of loop run. We use this on the DCM algorithm (gyro integration time)
    else
      G_Dt = 0;

    // *** DCM algorithm
    // Data adquisition
    Read_Gyro();   // This read gyro data
    Read_Accel();     // Read I2C accelerometer

    if (counter > 5)  // Read compass data at 10Hz... (5 loop runs)
    {
      counter = 0;
      Read_Compass();    // Read I2C magnetometer
      Compass_Heading(); // Calculate magnetic heading
    }

    // Calculations...
    Matrix_update();
    Normalize();
    Drift_correction();
    Euler_angles();
    // ***

    printdata();
  }

}
