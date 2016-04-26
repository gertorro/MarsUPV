using UnityEngine;
using UnityEngine.UI;
using System;
using System.Net;
using System.Net.Sockets;


public class OscServer : MonoBehaviour
{
    public int listenPort = 57130;
    public bool isactiveProcessing = true;

	//objetos del canvas

	public Text Temperature;
	public Text Pressure;
	public Text Altitude;
	public Text Speed;
	public Text Date;
	public Text HeartRate;
	public Text Location;
	public Text Oxygen;
	public Text Fuel;
	private double fuel;
	private double o2;
    private double o22;
    private double speed;
	private double h;
	private double bat;
	private double luz;
	private double temp;
	private double speed0 = 0;
	private double h0 = 0;

    UdpClient udpClient;
    IPEndPoint endPoint;
    Osc.Parser osc = new Osc.Parser ();
    
    void Start ()
    {
        endPoint = new IPEndPoint (IPAddress.Any, listenPort);
        udpClient = new UdpClient (endPoint);
    }

    void Update ()
    {
        while (udpClient.Available > 0) {
            osc.FeedData (udpClient.Receive (ref endPoint));
        }
        float bat2=(float)bat;
        float h2 = (float)h;
        float luz2= (float)luz;
        float temp2= (float)temp;
        float heart;
        float v2 = 0;
        while (osc.MessageCount > 0) {
            var msg = osc.PopMessage ();

            var target = GameObject.Find (msg.path.Replace ("/", "_"));
            if (target) {
                target.SendMessage ("OnOscMessage", msg.data [0]);
            }

           // Debug.Log (msg);
           
            if (isactiveProcessing && msg.data[0]!=null)
            {
                bat2 = (float)msg.data[0];
                h2 = (float)msg.data[1];
				luz2 = (float)msg.data[2];
                temp2 = (float)msg.data[3];
                v2 = (float)msg.data[4];
               // Debug.Log(h2);
            }
        }
        if(bat2==0)
        {
            bat2 = (float)bat;
        }
        if (temp2 == 0)
        {
            temp2 =(float) temp;
        }
        o2 =(float) (bat2 * 100) / 12.6;
		fuel = 10.0 + (float)(bat2 * 100 / 12.6);
	    heart = (float)( 80.0 + (float)(bat2 * 10 / 12.6));
        h = h2;
        temp = temp2;
        bat = bat2;
        o22 = o2;
		double pow = -0.0009 * h;
        double t = 0;
        double p = 0;
		if (h > 7000) {
			t= -23.4 - 0.00222 * h;
			 p = 0.699 * (double)Mathf.Exp ((float)pow);
		} else {
			 t = -31 - 0.000998 * h;
			 p = 0.699 * (double)Mathf.Exp ((float)pow);	
		}

		string time =  System.DateTime.Now.ToString("dd MMMM,yyyy")+ "\n" + System.DateTime.Now.ToString("HH:mm:ss");
		string temperature = "Temperature" + "\n" + Math.Round((float)t,2) + " " + (char)176 + "C";
		string pressure = "Pressure" + "\n" + Math.Round((float)p,2) + " kPa";
		string heartrate =  "Heart rate" + "\n     " + Math.Round((float)heart, 0) + " bpm";
		string location = "22.8 N, 5 E";

		Altitude.text= "Altitude" + "\n" + Math.Round(h2,2) + " m";
		Oxygen.text = "O2" + "\n" + Math.Round(o2,2) + " %";
		Fuel.text = "Fuel" + "\n" + Math.Round(fuel,2) + " %";
		Date.text = time;
        Speed.text = "V. Speed" + "\n" + Math.Round(v2, 2) + "m/s";
		Temperature.text = temperature;
		Pressure.text = pressure;
		Location.text = location;
        HeartRate.text = heartrate;
    }
}