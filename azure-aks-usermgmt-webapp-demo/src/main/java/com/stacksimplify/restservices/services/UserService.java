package com.stacksimplify.restservices.services;

import java.util.List;
import java.util.Optional;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Service;

import com.stacksimplify.restservices.entities.User;

@Service
public interface UserService {
	
	@PreAuthorize("hasAnyRole('ADMIN')")
	List<User> getAllUsers();
	
	@PreAuthorize("hasAnyRole('ADMIN')")
	User createUser(User user);
	
	@PreAuthorize("hasAnyRole('ADMIN')")
	User updateUserById(Long id, User user);
	
	@PreAuthorize("hasAnyRole('ADMIN', 'USER')")
	void deleteUserById(Long id) ;
	
	@PreAuthorize("hasAnyRole('ADMIN', 'USER')")
	Optional<User> getUserById(Long id);
		
	@PreAuthorize("hasAnyRole('ADMIN', 'USER')")
	User getUserByUsername(String username);
	

}
