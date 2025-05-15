package com.stacksimplify.restservices.authorizationserver.users.entities;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

@Entity
@Table(name = "users")
public class User implements UserDetails {

	static final long serialVersionUID = 1L;

	@Id
	@Size(min = 3, max = 20)
	@Column(name = "username", nullable = false, unique = true)
	private String username;

//	@NotNull
//	@Size(min = 1)
	@Column(name = "password", nullable = false)
	private String password;

	@NotNull
	@Column(name = "enabled", nullable = false)
	private boolean enabled;

//	@NotNull
//	@Size(min = 1)
	@Column(name = "role", nullable = false)
	private String role;

	@NotNull
	@Size(min = 1)
	@Column(name = "email", nullable = false)
	private String email;

	@Size(min = 1, max = 20)
	@Column(name = "firstname", nullable = false)
	private String firstname;

	@Size(max = 20)
	@Column(name = "lastname", nullable = false)
	private String lastname;

	@Override
	public Collection<? extends GrantedAuthority> getAuthorities() {
		List<GrantedAuthority> authorities = new ArrayList<GrantedAuthority>();
		authorities.add(new GrantedAuthority() {
			@Override
			public String getAuthority() {
				return role;
			}
		});
		return authorities;
	}

	@Override
	public boolean isAccountNonExpired() {
		return true;
	}

	@Override
	public boolean isAccountNonLocked() {
		// we never lock accounts
		return true;
	}

	@Override
	public boolean isCredentialsNonExpired() {
		// credentials never expire
		return true;
	}

	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}

	public boolean isEnabled() {
		return enabled;
	}

	public void setEnabled(boolean enabled) {
		this.enabled = enabled;
	}

	public String getRole() {
		return role;
	}

	public void setRole(String role) {
		this.role = role;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
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

}
