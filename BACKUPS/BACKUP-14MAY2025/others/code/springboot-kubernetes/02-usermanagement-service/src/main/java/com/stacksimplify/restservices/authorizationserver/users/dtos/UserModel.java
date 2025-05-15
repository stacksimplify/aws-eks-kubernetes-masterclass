package com.stacksimplify.restservices.authorizationserver.users.dtos;

import com.fasterxml.jackson.annotation.JsonProperty;

public class UserModel {
	
	@JsonProperty("username")
	private String username;
	
	@JsonProperty("email")
	private String email;
	
	@JsonProperty("role")
	private String role;

	@JsonProperty("enabled")
	private boolean enabled;
	

	@JsonProperty("firstname")
	private String firstname;
	
	
	@JsonProperty("lastname")
	private String lastname;

	@JsonProperty("appversion")
	private String appversion;

	
	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	public String getRole() {
		return role;
	}

	public void setRole(String role) {
		this.role = role;
	}

	public boolean isEnabled() {
		return enabled;
	}

	public void setEnabled(boolean enabled) {
		this.enabled = enabled;
	}

	public String getFirstname() {
		return firstname;
	}

	public void setFirstname(String firstname) {
		this.firstname = firstname;
	}

	public String getLastname() {
		return lastname;
	}

	public void setLastname(String lastname) {
		this.lastname = lastname;
	}

	public String getAppversion() {
		return appversion;
	}

	public void setAppversion(String appversion) {
		this.appversion = appversion;
	}

	
	
	
}
