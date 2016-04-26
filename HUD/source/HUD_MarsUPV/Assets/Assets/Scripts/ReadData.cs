using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System.IO;
using System;
using System.Net;


public class ReadData : MonoBehaviour
{
	private double t;
	private double p;
	public Text Temperature;
	public Text Pressure;
	public Text Altitude;
	public Text Speed;
	public Text Time;
	public Text HeartRate;
	public Text Location;
	public Text Oxygen;
	public Text Fuel;
	private double f;
	private double o2;
	private double speed;
	private double h;

	// Use this for initialization
	void Start()
	{ 
		InvokeRepeating("Actualiza", 1.0F, 1.0F);
	}
	
	void Actualiza()
	{
		string heartrate =  "Heart rate" + "\n     " + UnityEngine.Random.Range (80, 95) + " bpm";
		f = f - 0.32;
		o2 = o2 - 0.26;
		HeartRate.text = heartrate;
		Oxygen.text = "O2" + "\n" + Math.Round(o2,2) + " %";
		Fuel.text = "Fuel" + "\n" + Math.Round(f,2) + " %";
	}


	IEnumerator read()
	{
	  yield return new WaitForSeconds(1);
	
	}

	// Update is called once per frame
	void Update()
	{
		//read ();

		//speed = "Speed" + "\n" + speed + " m/s";
		//double h = double.Parse(tmpReader.ReadLine());
		double pow = -0.0009 * h;
		if (h > 7000) {
			t= -23.4 - 0.00222 * h;
			p = 0.699 * (double)Mathf.Exp ((float)pow);
		} else {
			t = -31 - 0.000998 * h;
			p = 0.699 * (double)Mathf.Exp ((float)pow);	
		}
		string time =  System.DateTime.Now.ToString("dd MMMM,yyyy")+ "\n" + System.DateTime.Now.ToString("HH:mm:ss");
		string altitude = "Altitude" + "\n" + Math.Round(h,2) + " m";
		string temperature = "Temperature" + "\n" + Math.Round(t,2) + " " + (char)176 + "C";
		string pressure = "Pressure" + "\n" + Math.Round(p,2) + " kPa";
		string location = "22.8 N, 5 E";

		//tmpReader.Close ();


		Temperature.text = temperature;
		Pressure.text = pressure;
		//Speed.text = speed;
		Altitude.text = altitude;
		Time.text = time;
		Location.text = location;

	}
}