package com.stacksimplify.restservices.services;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import com.stacksimplify.restservices.entities.User;
import com.stacksimplify.restservices.repositories.UserRepository;

@Service
public class UserServiceImpl implements UserService {

	@Autowired
	private UserRepository userRepository;

	@Autowired
	private BCryptPasswordEncoder passwordEncoder;

	// getAllUsers Method
	public List<User> getAllUsers() {
		return userRepository.findAll();
	}

	// CreateUser Method
	public User createUser(User user) {
		String userPassword = user.getPassword();
		String encodedUserPassword = passwordEncoder.encode(userPassword);
		user.setPassword(encodedUserPassword);
		return userRepository.save(user);
	}

	// getUserById
	public Optional<User> getUserById(Long id) {
		Optional<User> user = userRepository.findById(id);

		return user;
	}

	// updateUserById
	public User updateUserById(Long id, User user) {
		user.setUserid(id);
		return userRepository.save(user);

	}

	// deleteUserById
	public void deleteUserById(Long id) {
		if (userRepository.findById(id).isPresent()) {
			userRepository.deleteById(id);

		}
	}

	// getUserByUsername

	public User getUserByUsername(String username) {
		return userRepository.findByUsername(username);
	}

}
