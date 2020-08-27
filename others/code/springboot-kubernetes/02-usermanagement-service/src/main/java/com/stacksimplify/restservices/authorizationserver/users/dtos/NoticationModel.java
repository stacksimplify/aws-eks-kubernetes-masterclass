package com.stacksimplify.restservices.authorizationserver.users.dtos;

import com.fasterxml.jackson.annotation.JsonProperty;

public class NoticationModel {
	
	@JsonProperty("servicename")
	private String servicename;
	
	@JsonProperty("status")
	private String status;

	public String getServicename() {
		return servicename;
	}

	public void setServicename(String servicename) {
		this.servicename = servicename;
	}

	public String getStatus() {
		return status;
	}

	public void setStatus(String status) {
		this.status = status;
	}
	
	
	
	
	
}
