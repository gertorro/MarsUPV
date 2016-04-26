/*NASA SpaceApps 2016
 Mars UPV Team  http://www.marsupv.com/
 Code for Teensy 3.2 recieviing info through HWSerial 1 from a Bluetooth Serial bridge.
 Emulates a HID device and a Serial port for KSP controlling and Unity data connections.
 Shared under GNU GPL 3 http://www.gnu.org/licenses/gpl-3.0.en.html
*/
#define HWSERIAL Serial1
byte buffer_null[8];
volatile int joy0 = 0, joy1 = 0, joy2 = 0, joy3 = 0, rumbo = 0, pitch = 0, rumbo_1 = 0, pitch_1 = 0, temp = 0, ldr = 0;
float bateria = 0.0;
bool s1 = false, s2 = false, s3 = false, s4 = false;
long tini = 0, t_emp = 0;
void setup() {
  HWSERIAL.begin(38400);
  Serial.begin(38400);
  Joystick.useManualSend(true);
  //  HWSERIAL.setTimeout(100);
  tini = millis();
}

void loop() {
  rumbo_1 = rumbo;
  pitch_1 = pitch;
  String recibido = "";
  // read analog inputs and set X-Y position
  if (HWSERIAL.available() > 8)
  {
    int indice = 0, indice_1 = 0, i = 0;
    float valores_recibidos[13];

    recibido = HWSERIAL.readStringUntil('\n');
    //Serial.println(recibido.length());
    while (indice < recibido.length())
    { indice_1 = indice + 1;
      indice = recibido.indexOf(',', indice_1);
      //Serial.println(recibido.substring(indice_1, indice));
      valores_recibidos[i] = recibido.substring(indice_1, indice).toFloat();

      i++;
    }
    joy0 = int(valores_recibidos[1]);
    joy1 = int(valores_recibidos[2]);
    joy2 = int(valores_recibidos[3]);
    joy3 = int(valores_recibidos[4]);
    rumbo = int(valores_recibidos[5]);
    pitch = int(valores_recibidos[6]);
    bateria = valores_recibidos[7];
    s1 = int(valores_recibidos[8]);
    s2 = int(valores_recibidos[9]);
    s3 = int(valores_recibidos[10]);
    s4 = int(valores_recibidos[11]);
    temp = int(valores_recibidos[12]);
    ldr = int(valores_recibidos[13]);
    Joystick.X(joy0);//0
    Joystick.Y(joy1);//1
    Joystick.Z(joy2);//2
    Joystick.Zrotate(joy3);//3
    t_emp = millis() - tini;
    tini = 0;
    const int max_delta = 300;
    Joystick.sliderLeft(((rumbo-rumbo_1))*75+512); //4
    Joystick.sliderRight((pitch-pitch_1)*75+512); //5
    // read the digital inputs and set the buttons
    Joystick.button(1, s1);
    Joystick.button(2, s2);
    Joystick.button(3, s3);
    Joystick.button(4, s4);
    Joystick.send_now();
if(joy3>=750)
{
  s1=1;
}
else
{
  s1=0;
}
    Serial.print("MARSUPV,");
    Serial.print(bateria); //BatLvl
    Serial.print(',');
    Serial.print(s1);//Bot 1
    Serial.print(',');
    Serial.print(ldr); //LDR
    Serial.print(',');
    Serial.print(temp); //Temp
    Serial.println();

  }
}
