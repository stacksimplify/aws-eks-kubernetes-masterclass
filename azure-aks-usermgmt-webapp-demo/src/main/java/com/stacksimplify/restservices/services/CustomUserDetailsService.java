package com.stacksimplify.restservices.services;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import com.stacksimplify.restservices.entities.User;
import com.stacksimplify.restservices.repositories.UserRepository;

@Service
public class CustomUserDetailsService  implements UserDetailsService {

	@Autowired
	private UserRepository userRepository;
	
	private final Logger log1 = LoggerFactory.getLogger(this.getClass());
	
	@Override
	public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
		
		
		 log1.info("In CustomUserDetailsService class");
		User user = userRepository.findByUsername(username);
		CustomUserDetails userDetails = null;
		
		if(user != null) {
		userDetails = new CustomUserDetails();
		userDetails.setUser(user);
			
		} else {
			throw new UsernameNotFoundException("User not found with username as: "+username);
		}
		return userDetails;
		
	}

}
