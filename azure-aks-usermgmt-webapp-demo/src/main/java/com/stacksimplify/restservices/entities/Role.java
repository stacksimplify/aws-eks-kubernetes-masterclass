package com.stacksimplify.restservices.entities;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "role")
public class Role {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long roleid;
	private String role;

	public Role() {

	}
	
	

	public Role(Long roleid, String role) {
		super();
		this.roleid = roleid;
		this.role = role;
	}



	public Long getRoleid() {
		return roleid;
	}

	public void setRoleid(Long roleid) {
		this.roleid = roleid;
	}

	public String getRole() {
		return role;
	}

	public void setRole(String role) {
		this.role = role;
	}



	@Override
	public String toString() {
		return "Role [roleid=" + roleid + ", role=" + role + "]";
	}

	
	
	
}
