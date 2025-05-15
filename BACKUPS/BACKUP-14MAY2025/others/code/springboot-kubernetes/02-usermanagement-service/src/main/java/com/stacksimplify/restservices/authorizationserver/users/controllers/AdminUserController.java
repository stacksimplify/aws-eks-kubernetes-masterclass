package com.stacksimplify.restservices.authorizationserver.users.controllers;

import javax.validation.Valid;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import com.stacksimplify.restservices.authorizationserver.users.entities.User;
import com.stacksimplify.restservices.authorizationserver.users.repositories.UserRepository;
import com.stacksimplify.restservices.authorizationserver.users.services.UserService;

@RestController
public class AdminUserController {
	private static final Log logger = LogFactory.getLog(UserController.class);

	@Autowired
	private UserRepository userRepository;

	@Autowired
	private BCryptPasswordEncoder passwordEncoder;

	@Autowired
	private UserService userService;

	@PostMapping("/adminuser")
	@ResponseStatus(HttpStatus.OK)
	public void createUser(@RequestBody @Valid User user) {

		if (userRepository.findById(user.getUsername()).isPresent()) {
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
					String.format("User with user name %s already exists!", user.getUsername()));
		}
		if (userRepository.countByEmail(user.getEmail()) != 0) {
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
					String.format("User with email %s already exists!", user.getEmail()));
		}
		if (userService.matchesPolicy(user.getPassword()) == false) {
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
					String.format("User Password is invalid", user.getPassword()));
		}
		user.setPassword(passwordEncoder.encode(user.getPassword()));
		userRepository.save(user);
	}


}
