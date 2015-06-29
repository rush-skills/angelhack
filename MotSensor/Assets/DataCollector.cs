using UnityEngine;
using System.Collections;
using System.Net;
using System.Net.Sockets;

public class DataCollector : MonoBehaviour {

//	int[] buffer60 = new int[61];
	int f=0;
	//public Connector test=new Connector();
	Vector3 d= new Vector3(0f,0f,0f), v = new Vector3(0f,0f,0f),ac2=Vector3.zero;
	string S = "";
	// Use this for initialization

	Socket m_Socket;
	string m_IPAdress ="192.168.173.18";
	int kPort = 9126;
	bool p2 = false;
	string prev;
	bool leftPress, rightPress, touchLeft, touchRight;


	void Start () {
		S = "APal";
		//Send ("Palash");
		//new WWW ("http://10.60.21.142:5556/" + S);
		m_Socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
		System.Net.IPAddress    remoteIPAddress  = System.Net.IPAddress.Parse(m_IPAdress);
		System.Net.IPEndPoint   remoteEndPoint = new System.Net.IPEndPoint(remoteIPAddress, kPort);
		m_Socket.Connect(remoteIPAddress, 9126);
	}

	void Send(string msgData)
	{
		if (m_Socket == null) {
			Debug.Log("asd");
			return;
		}
		System.Text.UTF8Encoding encoding = new System.Text.UTF8Encoding();
		byte[] sendData = encoding.GetBytes(msgData);
		Debug.Log( m_Socket.Send(sendData));
	}

	// Update is called once per frame
	void FixedUpdate () {

		int n = Input.touchCount;
		touchLeft = touchRight = false;
		for (int i=0; i<n; i++) {
			Debug.Log(Input.GetTouch(i).position);
			if(Input.GetTouch(i).position.y<Screen.height/2) touchLeft = true;
			else touchRight = true;
		}

		Vector3 ac = Input.gyro.gravity;
		if (ac.x < -0.7)
			S = "Steady";
		else if (ac.z < -0.3 && ac.y < -0.3)
			S = "UpRight";
		else if (ac.z > 0.3 && ac.y > 0.3)
			S = "DownLeft";
		else if (ac.z < -0.3 && ac.y > 0.3)
			S = "DownRight";
		else if (ac.z > 0.3 && ac.y < -0.3)
			S = "UpLeft";
		else if (ac.y < -0.7)
			S = "Up";
		else if (ac.z < -0.7)
			S = "Right";
		else if (ac.z > 0.7)
			S = "Left";
		else if (ac.y > 0.7)
			S = "Down";
		else
			S = "Steady";
	//	S += "-";

		string S2="";
		if (!leftPress && (Input.GetKey (KeyCode.A)||touchLeft)) {
			leftPress = true;
			S2+="ADown";
		}
		if (!rightPress && (Input.GetKey (KeyCode.S)||touchRight)) {
			rightPress = true;
			S2+="BDown";
		}
		if ((!Input.GetKey (KeyCode.A)&&!touchLeft)&&leftPress) {
			leftPress = false;
			S2+="AUp";
		}
		if ((!Input.GetKey (KeyCode.S)&&!touchRight) && rightPress) {
			rightPress = false;
			S2+="BUp";
		}
		if (p2)
			S += "2";
		if (!S.Equals (prev)) {
			//new WWW ("10.60.21.142:5556/" + S);
			Send (S);
			Debug.Log(S);
			//S+= "\n"+ac+"\n"+Input.acceleration.sqrMagnitude;
		}
		if (!S2.Equals ("")) {
			if (p2)
				S2 += "2";
			Send (S2);
		}
		prev = S;
	}

	void OnGUI(){
		GUIStyle s = new GUIStyle();
		s.fontSize = 48;
		s.normal.textColor = Color.white;
		GUI.Label (new Rect (0, 0, Screen.width, Screen.height), S, s);
		if (GUI.Button (new Rect (420,140,480,120), "2ndPlayer",s)) {
			Input.gyro.enabled = true;
			p2=true;
		}
		if (GUI.Button (new Rect (420,270,480,220), "ResetConn",s)) {
			Input.gyro.enabled = true;
			m_Socket.Close();
			m_Socket = null;
			m_Socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
			System.Net.IPAddress    remoteIPAddress  = System.Net.IPAddress.Parse(m_IPAdress);
			System.Net.IPEndPoint   remoteEndPoint = new System.Net.IPEndPoint(remoteIPAddress, kPort);
			m_Socket.Connect(remoteIPAddress, 9126);
		}
		m_IPAdress = GUI.TextField(new Rect(10, 610, 500, 40), m_IPAdress,s);
		//m_IPAdress = GUI.TextField(new Rect(10, 610, 500, 40), m_IPAdress,s);
	}
	void OnApplicationQuit ()
	{
		m_Socket.Close();
		m_Socket = null;
	}
}
