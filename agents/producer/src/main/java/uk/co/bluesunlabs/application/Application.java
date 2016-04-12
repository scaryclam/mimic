package uk.co.bluesunlabs.application;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
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
	private HashMap<String, JSONObject> agentJobs;
	private HashMap<Future, Job> runningJobs;
	private HashMap<String, Job> cleanupJobs;
	private static final String[] acceptedJobTypes = new String[]{"http_producer", "rabbit_producer"};
	private Integer requestDelay = 10;
	private Integer checkDelay = 2;
	
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
	
	private JSONArray requestJobs() throws IOException, JSONException, NoJobsException, URISyntaxException {
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
			JSONArray newJobs = new JSONArray();
			
			if (jobs.length() < 1) {
				System.out.println("No jobs found, will retry later");
				throw new NoJobsException("No jobs found");
			} else {
				for (int index = 0; index < jobs.length(); index++) {
					JSONObject jobConfig = jobs.getJSONObject(index);
					String jobId = jobConfig.getString("job_id");
					if (!agentJobs.containsKey(jobId)) {
						agentJobs.put(jobId, jobConfig);
						newJobs.put(jobConfig);
					}
				}
				return newJobs;
			}
			
		} catch (JSONException error) {
			throw error;
		}
	}
	
	private void startJobs(JSONArray jobs) {
		// For each job in agentJobs, pull out the config, create a new job, and set a worker running the job
		JobFactory factory = new JobFactory();
		
		for (int index = 0; index < jobs.length(); index++) {
            JSONObject jobConfig = jobs.getJSONObject(index);
            Job job = factory.getJob(jobConfig);
            
            ExecutorService executor = Executors.newFixedThreadPool(2);
            Future<String> future = executor.submit(job);
            
            runningJobs.put(future, job);
			
			Thread thread = new Thread();
			thread.start();
		}
	}
	
	private void cleanUpJob(Job job) throws URISyntaxException, ClientProtocolException, IOException {
		cleanupJobs.put(job.getId(), job);
		String targetUrl = "http://" + serverHost + ":" + serverPort + "/job/release/";  
		System.out.println("Target url: " + targetUrl);
		URI url = new URI(targetUrl);
		HttpClient client = HttpClientBuilder.create().build();
		HttpPost post = new HttpPost(url);
		
		post.setHeader("User-Agent", USER_AGENT);
		List<NameValuePair> urlParameters = new ArrayList<NameValuePair>();
		urlParameters.add(new BasicNameValuePair("job_id", job.getId()));
		
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
		agentJobs.remove(job.getId());
		cleanupJobs.remove(job.getId());
	}
	
	private void checkJobs() throws InterruptedException, ExecutionException, ClientProtocolException, URISyntaxException, IOException {
		// Create as a separate object as we'll want to modify runningJobs
		HashMap<Future, Job> currentjobs = (HashMap<Future, Job>) runningJobs.clone();
		
		for (Map.Entry<Future, Job> entry : currentjobs.entrySet()) {
			Future future = entry.getKey();
            // Check if the job has finished
			if (future.isDone()) {
				// Shut down and pop off of the runningJobs
				String result = (String) future.get();
				runningJobs.remove(future);
				Job job = entry.getValue();
				cleanUpJob(job);
			}
		}
	}
	
	private void run() throws InterruptedException, ExecutionException {
		Runnable getJobsRunnable = new Runnable() {
	        public void run() {
	        	JSONArray jobs;
				try {
					jobs = getJobs();
					startJobs(jobs);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
	        }
	    };
	    
	    Runnable checkJobsRunnable = new Runnable() {
	        public void run() {
	        	try {
					checkJobs();
				} catch (InterruptedException | ExecutionException | URISyntaxException | IOException e) {
					e.printStackTrace();
				}
	        }
	    };
	    
	    ScheduledExecutorService service = Executors.newSingleThreadScheduledExecutor();
        service.scheduleAtFixedRate(getJobsRunnable, 0, requestDelay, TimeUnit.SECONDS);
        service.scheduleAtFixedRate(checkJobsRunnable, 0, checkDelay, TimeUnit.SECONDS);

	}
	
	private JSONArray getJobs() throws InterruptedException {
		while(true) {
		    try {
		    	System.out.println("Requesting jobs");
		    	JSONArray jobs = requestJobs();
		    	return jobs;
		    } catch (NoJobsException|IOException|JSONException|URISyntaxException err) {
				System.out.println("Caught exception, sleeping before retry...");
				System.out.println("Exception was " + err);
				Thread.sleep(10000);
			}
		}
	}
			
	public static void main(String[] args) throws InterruptedException, JSONException, IOException, ExecutionException {
		System.out.println("Starting...");
		agentId = UUID.randomUUID().toString();
		Application agent = new Application();
		agent.runningJobs = new HashMap<Future, Job>();
		agent.agentJobs = new HashMap<String, JSONObject>();
		agent.cleanupJobs = new HashMap<String, Job>();
		
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
		
		agent.run();
		System.out.println("Goodbye");
	}
}
