package com.stacksimplify.notifications.entities;

public class HelloMessage {
	
	private String applicationname;
	private String appversion;
	private String message;
	
	

	public String getApplicationname() {
		return applicationname;
	}
	public void setApplicationname(String applicationname) {
		this.applicationname = applicationname;
	}
	public String getAppversion() {
		return appversion;
	}
	public void setAppversion(String appversion) {
		this.appversion = appversion;
	}
	public String getMessage() {
		return message;
	}
	public void setMessage(String message) {
		this.message = message;
	}
	public HelloMessage(String applicationname, String appversion, String message) {
		super();
		this.applicationname = applicationname;
		this.appversion = appversion;
		this.message = message;
	}
	

	


	

}
