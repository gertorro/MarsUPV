/* NASA SpaceApps 2016
 Mars UPV Team
 Bridge code for Mars UPV's jetpack concept prop. Developed for NASA SpaceApps 2016.
 http://www.marsupv.com/
 Shared under GNU GPL 3 http://www.gnu.org/licenses/gpl-3.0.en.html
 */

import oscP5.*;
import netP5.*;
import processing.serial.*;

OscP5 oscP5;
NetAddress myRemoteLocation;
String read_string;
PImage img, img2;
Serial serial_port;
public float[] buffer=new float[5];
public double altitude=0.0;
public double speed=0.0;

void setup() {
    size(512, 1024);
    background(0);
    oscP5 = new OscP5(this, 57131);
    myRemoteLocation = new NetAddress("127.0.0.1", 57130);
    serial_port=new Serial(this, Serial.list()[0], 38400);//Change this line to the specifics of your system
    read_string="";

    img = loadImage("makersupv.png");
    img2 = loadImage("marsupv.jpg");
    color(255);
    textSize(100);
    text("Mars UPV", 10, 110);
    text("Team", 10, 220);
    image(img2, 0, 10, width, height/2.5);
    image(img, 0, height/2, width, height/2);
    serial_port.clear();//Clears the port before starting
}

void draw()
{
    if (serial_port.available()>0)//Waits for input
    {
        read_string=serial_port.readStringUntil(10);   //Reads until line break
        if (read_string!=null)//If data is valid...
        {
            String[] sep=split(read_string, ',');//Split the data by commas

            for (int i=1; i<sep.length; i++)
            {
                buffer[i-1]=float(sep[i]);//Loads the data into a buffer
            }

            // Vertical speed calculations
            if (buffer[1]>0.1) //If thrust is applied
            {
                speed+=1/20.0;
                altitude+=speed*1/20;
            } else //we fall down
            {
                speed-=3.71/20.0;
                altitude+=speed*1/20;
                if (altitude<=0)
                {
                    altitude=0.0;
                    speed=0.0;
                }
            }
            buffer[1] = (float)altitude; //Parse the data
            buffer[4] = (float)speed;
            sendValues(); //Send the values via UDP
        }
    }
}

void sendValues() {
    OscMessage oscCapa =new OscMessage("/JETPACK");
    OscMessage oscMess3 = new OscMessage("/data");
    oscMess3.add(buffer);
    oscP5.send(oscMess3, myRemoteLocation);
}
