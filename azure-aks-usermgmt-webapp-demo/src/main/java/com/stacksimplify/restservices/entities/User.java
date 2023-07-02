package com.stacksimplify.restservices.entities;

import java.util.Set;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.OneToMany;
import javax.persistence.SequenceGenerator;
import javax.persistence.Table;

import com.fasterxml.jackson.annotation.JsonIgnore;

//Entity 
// and
@Entity
@Table(name = "user")
public class User {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	//@GeneratedValue
	//Reference https://thoughts-on-java.org/jpa-generate-primary-keys/
	//@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "user_generator")
	//@SequenceGenerator(name="user_generator", sequenceName = "user_seq", allocationSize=50)
	private Long userid;

	@Column(name = "USER_NAME", length = 50, nullable = false, unique = true)
	private String username;

	@Column(name = "FIRST_NAME", length = 50, nullable = false)
	private String firstname;

	@Column(name = "LAST_NAME", length = 50, nullable = false)
	private String lastname;

	@Column(name = "EMAIL_ADDRESS", length = 50, nullable = false)
	private String email;

	@Column(name = "SSN", length = 50, nullable = false, unique = true)
	private String ssn;
	
	@Column(name = "PASSWORD")
	private String password;

	@OneToMany(cascade = CascadeType.ALL, fetch = FetchType.EAGER)
	@JoinTable(name = "user_role", joinColumns = @JoinColumn(name = "userid"), inverseJoinColumns = @JoinColumn(name = "roleid"))
	private Set<Role> roles;

	public User() {

	}
	
	

	public User(Long userid, String username, String firstname, String lastname, String email, String ssn,
			String password, Set<Role> roles) {
		super();
		this.userid = userid;
		this.username = username;
		this.firstname = firstname;
		this.lastname = lastname;
		this.email = email;
		this.ssn = ssn;
		this.password = password;
		this.roles = roles;
	}



	public Long getUserid() {
		return userid;
	}

	public void setUserid(Long userid) {
		this.userid = userid;
	}

	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
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

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	public String getSsn() {
		return ssn;
	}

	public void setSsn(String ssn) {
		this.ssn = ssn;
	}

	public Set<Role> getRoles() {
		return roles;
	}

	public void setRoles(Set<Role> roles) {
		this.roles = roles;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}



	@Override
	public String toString() {
		return "User [userid=" + userid + ", username=" + username + ", firstname=" + firstname + ", lastname="
				+ lastname + ", email=" + email + ", ssn=" + ssn + ", password=" + password + ", roles=" + roles + "]";
	}

	
	
	
}
