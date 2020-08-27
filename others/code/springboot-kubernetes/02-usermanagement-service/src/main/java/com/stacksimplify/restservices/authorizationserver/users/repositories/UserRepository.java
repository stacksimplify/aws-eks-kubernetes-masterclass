package com.stacksimplify.restservices.authorizationserver.users.repositories;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import com.stacksimplify.restservices.authorizationserver.users.entities.User;

public interface UserRepository extends JpaRepository<User, String> {

	public long countByEmail(String email);

	@Query("select u.username from User u where u.role = ?1")
	List<String> findUsernamesByRole(String role);

	@Query("select u.email from User u where u.role = ?1")
	List<String> findEmailsByRole(String role);

	@Query("select u.email from User u where u.username = ?1")
	String findEmailByUsername(String username);
}