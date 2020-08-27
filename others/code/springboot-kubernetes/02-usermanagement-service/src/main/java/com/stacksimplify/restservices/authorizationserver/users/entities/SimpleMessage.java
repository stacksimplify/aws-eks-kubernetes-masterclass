package com.stacksimplify.restservices.authorizationserver.users.entities;

public class SimpleMessage {
	
	private String message;
	private String appversion;
	public SimpleMessage(String message, String appversion) {
		super();
		this.message = message;
		this.appversion = appversion;
	}
	public String getMessage() {
		return message;
	}
	public void setMessage(String message) {
		this.message = message;
	}
	public String getAppversion() {
		return appversion;
	}
	public void setAppversion(String appversion) {
		this.appversion = appversion;
	}

	


	

}
