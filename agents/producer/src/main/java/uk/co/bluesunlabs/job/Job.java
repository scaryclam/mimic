package uk.co.bluesunlabs.job;

import java.util.concurrent.Callable;
import java.util.concurrent.Future;

import com.json.JSONObject;


public interface Job extends Callable<String> {	
	public String getId();
}
