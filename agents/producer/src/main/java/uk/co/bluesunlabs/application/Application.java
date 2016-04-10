package uk.co.bluesunlabs.application;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.message.BasicNameValuePair;

import uk.co.bluesunlabs.job.Job;
import uk.co.bluesunlabs.job.JobFactory;

import com.json.JSONArray;
import com.json.JSONException;
import com.json.JSONObject;


public class Application {
	private static final String USER_AGENT = "Mimic Agent 1.0";
	private String serverHost = "localhost";
	private Integer serverPort = 8877;
	private static String agentId;
	private Boolean isRegistered = false;
	private JSONArray agentJobs;
	private static final String[] acceptedJobTypes = new String[]{"http_producer", "rabbit_producer"};
	
	private class NoJobsException extends Exception {
		private static final long serialVersionUID = -8115941090831065970L;

		public NoJobsException(String message) {
	        super(message);
	    }
	}
	
	private void register() throws IOException, JSONException, URISyntaxException {
		String targetUrl = "http://" + serverHost + ":" + serverPort + "/agent/register/";  
		System.out.println("Target url: " + targetUrl);
		URI url = new URI(targetUrl);
		HttpClient client = HttpClientBuilder.create().build();
		HttpPost post = new HttpPost(url);
		
		post.setHeader("User-Agent", USER_AGENT);
		List<NameValuePair> urlParameters = new ArrayList<NameValuePair>();
		for (String value: acceptedJobTypes) {
			urlParameters.add(new BasicNameValuePair("job_types", value));
		}
		
		post.setEntity(new UrlEncodedFormEntity(urlParameters));

		HttpResponse response = client.execute(post);
		

		BufferedReader in = new BufferedReader(
		    new InputStreamReader(response.getEntity().getContent()));
		String inputLine;
		StringBuffer result = new StringBuffer();

		while ((inputLine = in.readLine()) != null) {
			result.append(inputLine);
		}
		System.out.println(response.toString());
		in.close();
		try {
			JSONObject regData = new JSONObject(result.toString());
			agentId = regData.getString("identifier");
		} catch (JSONException error) {
			isRegistered = false;
			throw error;
		}
		isRegistered = true;
		System.out.println("Registered as " + agentId);
	}
	
	private void requestJobs() throws IOException, JSONException, NoJobsException, URISyntaxException {
		String targetUrl = "http://" + serverHost + ":" + serverPort + "/agent/jobs/request";  
		System.out.println("Target url: " + targetUrl);
		URI url = new URI(targetUrl);
		
		HttpClient client = HttpClientBuilder.create().build();
		HttpGet request = new HttpGet(url);
		request.addHeader("User-Agent", USER_AGENT);
		request.addHeader("AGENT_ID", agentId);
		HttpResponse response = client.execute(request);

		BufferedReader in = new BufferedReader(
		    new InputStreamReader(response.getEntity().getContent()));

		StringBuffer result = new StringBuffer();
		String inputLine = "";

		while ((inputLine = in.readLine()) != null) {
			result.append(inputLine);
		}
		System.out.println(result.toString());
		in.close();
		
		System.out.println(response.getStatusLine());
		try {
			JSONObject jobsData = new JSONObject(result.toString());
			JSONArray jobs = jobsData.getJSONArray("jobs");
			
			if (jobs.length() < 1) {
				System.out.println("No jobs found, will retry later");
				throw new NoJobsException("No jobs found");
			} else {
				agentJobs = jobs; 
			}
			
		} catch (JSONException error) {
			throw error;
		}
	}
	
	private void run() {
		// For each job in agentJobs, pull out the config, create a new job, and set a worker running the job
		JobFactory factory = new JobFactory();
		for (int index = 0; index < agentJobs.length(); index++) {
            JSONObject jobConfig = agentJobs.getJSONObject(index);
			Job job = factory.getJob(jobConfig);
			Thread thread = new Thread(job);
			thread.start();
		}
	}
			
	public static void main(String[] args) throws InterruptedException, JSONException, IOException {
		System.out.println("Starting...");
		agentId = UUID.randomUUID().toString();
		Application agent = new Application();
		while(true) {
			try {
				System.out.println("Attempting to register");
				agent.register();
				break;
			} catch (IOException|JSONException|URISyntaxException err) {
				System.out.println("Caught exception, sleeping before retry...");
				Thread.sleep(5000);
			}
		}
		while(true) {
		    try {
		    	System.out.println("Requesting jobs");
		    	agent.requestJobs();
		    	break;
		    } catch (NoJobsException|IOException|JSONException|URISyntaxException err) {
				System.out.println("Caught exception, sleeping before retry...");
				System.out.println("Exception was " + err);
				Thread.sleep(10000);
			}
		}
		agent.run();
		System.out.println("Goodbye");
	}
}
