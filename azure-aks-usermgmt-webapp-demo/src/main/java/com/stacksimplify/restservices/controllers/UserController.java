package com.stacksimplify.restservices.controllers;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.stacksimplify.restservices.entities.User;
import com.stacksimplify.restservices.services.UserService;

@RestController
@RequestMapping("/secure")
public class UserController {

	@Autowired
	private UserService userService;

	// get All Users
	@GetMapping("/admin/users/all")
	public List<User> getAllUsers() {

		return userService.getAllUsers();

	}

	// Create User
	@PostMapping("/admin/users/create")
	public User createUser(@RequestBody User user) {
		return userService.createUser(user);
	}

	// Update User By Id
	@PutMapping("/admin/users/update/{id}")
	public User updateUserById(@PathVariable("id") Long id, @RequestBody User user) {
		return userService.updateUserById(id, user);
	}

	// Delete User By Id
	@DeleteMapping("/admin/users/delete/{id}")
	public void deleteUserById(@PathVariable("id") Long id) {
		userService.deleteUserById(id);
	}

	// get User By Id
	@GetMapping("/users/{id}")
	public Optional<User> getUserById(@PathVariable("id") Long id) {
		return userService.getUserById(id);

	}

	// get User by Username
	@GetMapping("/users/byusername/{username}")
	public User getUserByUsername(@PathVariable("username") String username) {
		return userService.getUserByUsername(username);
	}

}
