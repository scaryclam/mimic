package uk.co.bluesunlabs.application;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.UUID;

import com.json.JSONArray;
import com.json.JSONObject;

public class Application {
	private String serverHost = "localhost";
	private Integer serverPort = 8877;
	private static String agentId;
	private Boolean isRegistered = false;
	
	private void register() throws IOException {
		String targetUrl = "http://" + serverHost + ":" + serverPort + "/agent/register/";  
		System.out.println("Target url: " + targetUrl);
		URL url = new URL(targetUrl);
		HttpURLConnection connection = (HttpURLConnection)url.openConnection();
		connection.setRequestMethod("POST");

		String urlParameters = "agent=" + agentId;
		
		// Send post request
		connection.setDoOutput(true);
		DataOutputStream outputStream = new DataOutputStream(connection.getOutputStream());
		outputStream.writeBytes(urlParameters);
		outputStream.flush();
		outputStream.close();

		BufferedReader in = new BufferedReader(
		    new InputStreamReader(connection.getInputStream()));
		String inputLine;
		StringBuffer response = new StringBuffer();

		while ((inputLine = in.readLine()) != null) {
			response.append(inputLine);
		}
		in.close();
		isRegistered = true;
	}
	
	private void run() {
		JSONArray jobConfig = new JSONArray();
		JSONObject JobOneConfig = new JSONObject();
		
	}
			
	public static void main(String[] args) throws InterruptedException {
		System.out.println("Starting...");
		agentId = UUID.randomUUID().toString();
		Application agent = new Application();
		while(true) {
			try {
				System.out.println("Attempting to register");
				agent.register();
				break;
			} catch (IOException err) {
				Thread.sleep(5000);
			}
		}
		agent.run();
		System.out.println("Goodbye");
	}
}
