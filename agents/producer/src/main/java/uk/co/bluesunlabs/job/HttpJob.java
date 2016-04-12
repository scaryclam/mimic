package uk.co.bluesunlabs.job;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.Future;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.HttpClientBuilder;

import com.json.JSONObject;

public class HttpJob implements Job {
	private String jobName;
	private String jobId;
	private String targetURI;
	private String targetMethod;
	private String targetPayload;
	private Map<String, String> targetGETParams;
	private static final String USER_AGENT = "Mimic Agent 1.0";
	
	private class HTTPMethodNotSupported extends Exception {

		public HTTPMethodNotSupported(String message) {
	        super(message);
	    }
	}
	
	public HttpJob(JSONObject config) {
		jobName = config.getString("name");
		jobId = config.getString("job_id");
		targetURI = config.getString("targetURI");
		targetMethod = config.getString("targetMethod");
		if (config.has("targetPayload")) {
			targetPayload = config.getString("targetPayload");
		}
	}
	
	private void sendPost() throws ClientProtocolException, IOException {
		HttpClient client = HttpClientBuilder.create().build();
		HttpPost request = new HttpPost(targetURI);
		request.setHeader("User-Agent", USER_AGENT);
		HttpResponse response = client.execute(request);
	}
	
	private void sendGet() throws ClientProtocolException, IOException {
		HttpClient client = HttpClientBuilder.create().build();
		HttpGet request = new HttpGet(targetURI);
		request.setHeader("User-Agent", USER_AGENT);
		HttpResponse response = client.execute(request);
	}
	
	private void runJob() throws HTTPMethodNotSupported, ClientProtocolException, IOException {
		
		if (targetMethod.equalsIgnoreCase("GET")) {
			sendGet();
		} else if (targetMethod.equalsIgnoreCase("POST")) {
			sendPost();
		} else {
			throw new HTTPMethodNotSupported("The method " + targetMethod + " is not supported");
		}
	}

	@Override
	public String call() {
		System.out.println("Running HTTP Job " + jobName);
		try {
			runJob();
		} catch (HTTPMethodNotSupported | IOException e1) {
			e1.printStackTrace();
		}
		try {
			Thread.sleep(10000);
			
		} catch (InterruptedException e) {
			
		}
		Thread.currentThread().interrupt();
		return "Done";
	}

	@Override
	public String getId() {
		return jobId;
	}
}
