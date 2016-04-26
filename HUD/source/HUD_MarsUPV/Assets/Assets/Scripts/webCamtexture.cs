using System;
using UnityEngine;
using UnityEngine.UI;
using System.IO;
using System.Collections;

public class webCamtexture : MonoBehaviour {

    public RawImage rawimage;

    void Start()
    {
		WebCamDevice[] devices = WebCamTexture.devices;
        WebCamTexture webcamTexture = new WebCamTexture(Screen.width, Screen.height, 60);
		webcamTexture.deviceName = devices [0].name;
		rawimage.texture = webcamTexture;
        rawimage.material.mainTexture = webcamTexture;
        webcamTexture.Play();
    }
    void Update()
    {

    }
}   