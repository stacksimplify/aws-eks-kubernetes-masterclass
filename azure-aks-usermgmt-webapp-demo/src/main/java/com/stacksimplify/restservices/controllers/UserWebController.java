package com.stacksimplify.restservices.controllers;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import javax.validation.Valid;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.propertyeditors.CustomDateEditor;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

import com.stacksimplify.restservices.entities.Role;
import com.stacksimplify.restservices.entities.User;
import com.stacksimplify.restservices.repositories.UserRepository;
import com.stacksimplify.restservices.services.UserService;

@Controller
public class UserWebController {

	@Autowired
	UserService userService;

	@Autowired
	UserRepository userRepository;

	
	private final Logger log = LoggerFactory.getLogger(this.getClass());

	
	// get Username from security context
	private String getSignedUser(ModelMap model) {
		Object principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();
		if (principal instanceof UserDetails) {
			return ((UserDetails) principal).getUsername();
		}
		return principal.toString();
	}

	/**
	 * This method will list all existing users.
	 */
	@RequestMapping(value = "/list-users", method = RequestMethod.GET)
	public String showUsers(ModelMap model) {
		String name = getSignedUser(model);
		model.put("users", userService.getAllUsers());
		return "list-users";
	}

	
	/**
	 * This method will provide the medium to add a new user.
	 */
	@RequestMapping(value = "/add-user", method = RequestMethod.GET)
	public String showAddUserPage(ModelMap model) {
		model.addAttribute("user", new User());
		model.addAttribute("edit", false);
		return "user";
	}
	
	/**
	 * This method will be called on form submission, handling POST request for
	 * saving user in mysql database.
	 */
	@RequestMapping(value = "/add-user", method = RequestMethod.POST)
	public String addUser(ModelMap model, @Valid User user, BindingResult result) {
		if (result.hasErrors()) {
			return "user";
		}
		Role role1 = new Role(null, "ADMIN");
		//Role role2 = new Role(null, "USER");
		Set<Role> set = Stream.of(role1).collect(Collectors.toSet());
		user.setRoles(set);
		userService.createUser(user);
		return "redirect:/list-users";
	}


	/**
	 * This method will provide the medium to update an existing user.
	 */
	@RequestMapping(value = "/update-user", method = RequestMethod.GET)
	public String showUpdateUserPage(@RequestParam Long userid, ModelMap model) {
		User user = userRepository.findById(userid).get();
		model.put("user", user);
		model.addAttribute("edit", true);
		return "user";
	}

	/**
	 * This method will be called on form submission, handling POST request for
	 * updating user in database. It also validates the user input
	 */
	@RequestMapping(value = "/update-user", method = RequestMethod.POST)
	public String updateUser(ModelMap model, @Valid User user, BindingResult result) {
		if (result.hasErrors()) {
			return "user";
		}
		userRepository.save(user);
		return "redirect:/list-users";
	}
	
	/**
	 * This method will delete an user by it's SSOID value.
	 */
	@RequestMapping(value = "/delete-user", method = RequestMethod.GET)
	public String deleteUser(@RequestParam Long userid) {
		userRepository.deleteById(userid);
		return "redirect:/list-users";
	}

	
	
}
