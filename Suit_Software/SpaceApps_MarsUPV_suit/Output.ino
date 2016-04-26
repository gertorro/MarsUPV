void printdata(void)
{
  if (send_servos)
  {
    servo1.write(map(analogRead(pin_Jostick1_X), 0, 1023, 135, 45));
    servo2.write(map(analogRead(pin_Jostick1_Y), 0, 1023, 45, 135));
    servo3.write(map(analogRead(pin_Jostick1_X), 0, 1023, 45, 135));
    servo4.write(map(analogRead(pin_Jostick1_Y), 0, 1023, 45, 135));
  }
  if (send_bluetooth) {
    Serial1.print("MARSUPV,");
    Serial1.print(analogRead(pin_Jostick1_X));
    Serial1.print(',');
    Serial1.print(analogRead(pin_Jostick1_Y));
    Serial1.print(',');
    Serial1.print(analogRead(pin_Jostick2_X));
    Serial1.print(',');
    Serial1.print(analogRead(pin_Jostick2_Y));
    Serial1.print(',');
    Serial1.print(int(ToDeg(yaw)));
    Serial1.print(',');
    Serial1.print(int(ToDeg(pitch)));
    Serial1.print(',');
    Serial1.print(float(analogRead(pin_Voltaje_3) * 14.0 / 1023.0));
    Serial1.print(',');
    Serial1.print(!digitalRead(pin_Pulsador_Jostick1));
    Serial1.print(',');
    Serial1.print(!digitalRead(pin_Pulsador_Jostick2));
    Serial1.print(',');
    Serial1.print(0);
    Serial1.print(',');
    Serial1.print(0);
    Serial1.print(',');
    Serial1.print(analogRead(pin_termistor_2));
    Serial1.print(',');
    Serial1.print((analogRead(pin_LDR_1) + analogRead(pin_LDR_2) + analogRead(pin_LDR_3) + analogRead(pin_LDR_4)) / 4);
    Serial1.println();
  }
  if (send_bluetooth) {
    Serial.print("MARSUPV,");
    Serial.print(analogRead(pin_Jostick1_X));
    Serial.print(',');
    Serial.print(analogRead(pin_Jostick1_Y));
    Serial.print(',');
    Serial.print(analogRead(pin_Jostick2_X));
    Serial.print(',');
    Serial.print(analogRead(pin_Jostick2_Y));
    Serial.print(',');
    Serial.print(int(ToDeg(yaw)));
    Serial.print(',');
    Serial.print(int(ToDeg(pitch)));
    Serial.print(',');
    Serial.print(float(analogRead(pin_Voltaje_3) * 14.0 / 1023.0));
    Serial.print(',');
    Serial.print(!digitalRead(pin_Pulsador_Jostick1));
    Serial.print(',');
    Serial.print(!digitalRead(pin_Pulsador_Jostick2));
    Serial.print(',');
    Serial.print(0);
    Serial.print(',');
    Serial.print(0);
    Serial.print(',');
    Serial.print(analogRead(pin_termistor_2));
    Serial.print(',');
    Serial.print((analogRead(pin_LDR_1) + analogRead(pin_LDR_2) + analogRead(pin_LDR_3) + analogRead(pin_LDR_4)) / 4);
    Serial.println();
  }
  if (test_bluetooth)
  {
    Serial.println("Enviando por bluetooth...");
    Serial1.print("MARSUPV,");
    Serial1.print(random(0, 1023)); //BatLvl
    Serial1.print(',');
    Serial1.print(random(0, 1023)); //BatLvl
    Serial1.print(',');
    Serial1.print(random(0, 1023)); //BatLvl
    Serial1.print(',');
    Serial1.print(random(0, 1023)); //BatLvl
    Serial1.print(',');
    Serial1.print(random(0, 1023)); //BatLvl
    Serial1.print(',');
    Serial1.print(random(0, 1023)); //BatLvl
    Serial1.print(',');
    Serial1.print(random(0, 1023)); //BatLvl
    Serial1.print(',');
    Serial1.print(random(0, 1)); //BatLvl
    Serial1.print(',');
    Serial1.print(random(0, 1)); //BatLvl
    Serial1.print(',');
    Serial1.print(random(0, 1)); //BatLvl
    Serial1.print(',');
    Serial1.print(random(0, 1)); //BatLvl
    Serial1.print(',');
    Serial1.print(random(0, 1023)); //BatLvl
    Serial1.print(',');
    Serial1.print(random(0, 1023)); //BatLvl
    Serial1.println();
  }
  if (!digitalRead(pin_Pulsador_Jostick1))
  {
    if (!leds_encendidos)
    {
      for(int j=0;j<256;j++){
      analogWrite(pin_led_4, j);
      analogWrite(pin_led_5, j);
      analogWrite(pin_led_6, j);
      analogWrite(pin_led_7, j);
      delay(10);
      }
     leds_encendidos=true;
    }
    else
    {
      leds_encendidos=false;
      for(int j=255;j>=0;j--){
      analogWrite(pin_led_4, j);
      analogWrite(pin_led_5, j);
      analogWrite(pin_led_6, j);
      analogWrite(pin_led_7, j);
      delay(10);
      }
    }
    delay(250);
  }

if (!digitalRead(pin_Pulsador_Jostick2))
  {
      analogWrite(pin_led_8, 255);
      for(int k=0;k<=180;k+=15)
      {
        servo5.write(k);
        delay(100);
      }
        for(int k=180;k>=0;k-=15)
      {
        servo5.write(k);
        delay(100);
      }
      digitalWrite(pin_led_8,0);
      servo5.write(90);
  }
  
  volatile int lectura = analogRead(pin_Jostick2_Y);
  if (lectura >= 512)
  {
    analogWrite(pin_led_2,(512-lectura)/2);
    analogWrite(pin_led_3,(128-lectura)/2);
    analogWrite(pin_led_1,(lectura-512)/2);
  }
  else
  {
    digitalWrite(pin_led_1, 0);
    digitalWrite(pin_led_2, 0);
    digitalWrite(pin_led_3, 0);
  }
}

long convert_to_dec(float x)
{
  return x * 10000000;
}



