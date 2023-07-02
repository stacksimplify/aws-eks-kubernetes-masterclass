package com.stacksimplify.restservices.services;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import com.stacksimplify.restservices.entities.User;

@Service
public class CustomUserDetails implements UserDetails {

	/**
	 * 
	 */
	private static final long serialVersionUID = -1701184685025573726L;
	
	
	
	private final Logger log1 = LoggerFactory.getLogger(this.getClass());
	


	private User user;
	
	@Override
	public Collection<? extends GrantedAuthority> getAuthorities() {
		/* List<SimpleGrantedAuthority> roledetails = user.getRoles()
														.stream()
														.map(role -> new SimpleGrantedAuthority("ROLE_"+role.getRole()))
														.collect(Collectors.toList());*/
		 
		List<SimpleGrantedAuthority> roledetails = user.getRoles()
					.stream()
					.map(role -> new SimpleGrantedAuthority("ROLE_ADMIN"))
					.collect(Collectors.toList());
		 
		 log1.info("Retruning role details from CustomUserDetails class");
		 
		 log1.info("Role Details: {}"+roledetails);
											 
		 return roledetails;
		
	}

	@Override
	public String getPassword() {
		return user.getPassword();
	}

	@Override
	public String getUsername() {
		
		return user.getUsername();
	}

	@Override
	public boolean isAccountNonExpired() {
		return true;
	}

	@Override
	public boolean isAccountNonLocked() {
		return true;
	}

	@Override
	public boolean isCredentialsNonExpired() {
		return true;
	}

	@Override
	public boolean isEnabled() {
		return true;
	}

	public User getUser() {
		return user;
	}

	public void setUser(User user) {
		this.user = user;
	}
	
	

	
	
	
}
