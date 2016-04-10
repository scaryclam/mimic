package uk.co.bluesunlabs.job;

import com.json.JSONObject;

public class JobFactory {
	private static final String JOB_TYPE = "http_producer";
	
	public Job getJob(JSONObject config) {
		String jobType = config.getString("job_type");
		if (jobType.equals(JOB_TYPE)) {
			HttpJob newJob = new HttpJob(config);
			return newJob;
		}
		return null;
	}
}
