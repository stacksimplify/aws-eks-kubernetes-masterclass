package com.stacksimplify.restservices.authorizationserver.users.controllers;

import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import javax.validation.Valid;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.util.Assert;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.server.ResponseStatusException;

import com.amazonaws.xray.spring.aop.XRayEnabled;

import com.stacksimplify.restservices.authorizationserver.users.dtos.EmailMessage;
import com.stacksimplify.restservices.authorizationserver.users.dtos.UserModel;
import com.stacksimplify.restservices.authorizationserver.users.entities.User;
import com.stacksimplify.restservices.authorizationserver.users.repositories.UserRepository;
import com.stacksimplify.restservices.authorizationserver.users.services.UserService;


import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.util.EntityUtils;
import com.amazonaws.xray.proxies.apache.http.HttpClientBuilder;



@RestController
@XRayEnabled
public class UserController {

	private static final Log logger = LogFactory.getLog(UserController.class);

	@Autowired
	private UserRepository userRepository;

	@Autowired
	private BCryptPasswordEncoder passwordEncoder;

	@Autowired
	private UserService userService;
	
    @Autowired
    private Environment env;
	
	@GetMapping("/health-status")
	public String healthStatus(){
		//String password = "password101"; 
		//PasswordEncoder passwordEncoder = new BCryptPasswordEncoder(); 
		//String encodedPassword = passwordEncoder.encode(password);
		//System.out.print(encodedPassword);
		return "User Management Service UP and RUNNING - V1";
		
	}
	
	//ALWAYS COMMENTED @PreAuthorize("hasAnyRole('ROLE_MODERATOR','ROLE_ADMIN')")
	@GetMapping("/users")
	@ResponseStatus(HttpStatus.OK)
	public List<UserModel> listAllUsers() {
		List<User> users = userRepository.findAll();
		List<UserModel> filteredUsers = users.stream().map(u -> {
			UserModel user = new UserModel();
			user.setUsername(u.getUsername());
			user.setEmail(u.getEmail());
			user.setRole(u.getAuthorities().stream().findFirst().get().getAuthority());
			user.setEnabled(u.isEnabled());
			user.setFirstname(u.getFirstname());
			user.setLastname(u.getLastname());
			user.setAppversion("V1");
			return user;
		}).collect(Collectors.toList());
		return filteredUsers;
	}

	// TO UNPROTECT @PreAuthorize("hasAnyRole('ROLE_MODERATOR','ROLE_ADMIN')")
	@GetMapping("/user/{username}")
	@ResponseStatus(HttpStatus.OK)
	public UserModel getUserByUsername(@PathVariable("username") String userName) {

		User user = userRepository.findById(userName)
				.orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND,
						String.format("User with user name %s doesn't exist!", userName)));

		UserModel userModel = new UserModel();
		userModel.setUsername(user.getUsername());
		userModel.setEmail(user.getEmail());
		userModel.setFirstname(user.getFirstname());
		userModel.setLastname(user.getLastname());
		userModel.setEnabled(user.isEnabled());
		userModel.setRole(user.getAuthorities().stream().findFirst().get().getAuthority());
		return userModel;
	}

	// TO UNPROTECT @PreAuthorize("hasAnyRole('ROLE_ADMIN')")
	@PostMapping("/user")
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
		sendAccountActivationNotifications(user);
	}

	// TO UNPROTECT @PreAuthorize("hasAnyRole('ROLE_ADMIN')")
	@PutMapping("/user")
	@ResponseStatus(HttpStatus.OK)
	public void updateUser(@RequestBody @Valid User user) {

		User u = userRepository.findById(user.getUsername())
				.orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND,
						String.format("User with user name %s doesn't exist!", user.getUsername())));

		// check email unique.
		if (u.getEmail().trim().equalsIgnoreCase(user.getEmail().trim()) == false
				&& userRepository.countByEmail(user.getEmail()) != 0) {
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
					String.format("User with email %s already exists!", user.getEmail()));
		}

		u.setEmail(user.getEmail());
		u.setFirstname(user.getFirstname());
		u.setLastname(user.getLastname());
		userRepository.save(u);
	}

	// TO UNPROTECT @PreAuthorize("hasAnyRole('ROLE_ADMIN')")
	@DeleteMapping("/user/{username}")
	@ResponseStatus(HttpStatus.OK)
	public void deleteUser(@PathVariable("username") String userName) {

		if (userRepository.findById(userName).isPresent()) {
			userRepository.deleteById(userName);
		} else {
			throw new ResponseStatusException(HttpStatus.NOT_FOUND,
					String.format("User with user name %s doesn't exist!", userName));
		}
	}

	// TO UNPROTECT @PreAuthorize("hasAnyRole('ROLE_ADMIN')")
	@GetMapping("/status/{username}")
	@ResponseStatus(HttpStatus.OK)
	public void changeUserStatus(@PathVariable("username") String userName) {

		User user = userRepository.findById(userName)
				.orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND,
						String.format("User with user name %s doesn't exist!", userName)));

		boolean state = !user.isEnabled();
		user.setEnabled(state);
		userRepository.save(user);
	}

	// TO UNPROTECT @PostMapping("/public/register")
	@ResponseStatus(HttpStatus.OK)
	public ResponseEntity<?> registerUser(@RequestBody @Valid User user) {

		// check if user with same name or email doesn't exist.
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


		user.setRole("ROLE_USER"); // registering users will always have role ROLE_USER.
		user.setPassword(passwordEncoder.encode(user.getPassword()));
		user.setEnabled(false);
		userRepository.save(user);
		
		HashMap<String, String> response = new HashMap<>();
		response.put("message",
				"Thank you for registering with StackSimplify User Management,  "
						+ "your account is created successfully and is pending activation,  "
						+ "you will be able to login once admin approve's and activates your account. ");
		return ResponseEntity.status(200).body(response);
	
	}

	// TO UNPROTECT @PreAuthorize("hasAnyRole('ROLE_ADMIN')")
	@GetMapping("/user/activate/{username}")
	@ResponseStatus(HttpStatus.OK)
	public void activateUser(@PathVariable("username") String userName) {

		User user = userRepository.findById(userName)
				.orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND,
						"User with user name " + userName + " doesn't exist!"));

		// if user account is not already activated, activate user account.
		Assert.isTrue(user.isEnabled() == false, "User already activated!");

		user.setEnabled(true);
		userRepository.save(user);

	}
	
	
    public void sendAccountActivationNotifications(User user) {
        // Send Email Notifications
        String userEmailContent = String.format("Hello %s, your stack simplify account is created successfully!", user.getFirstname());

		EmailMessage message = new EmailMessage();
		message.setSubject("Stack Simplify account creation.");
		message.setContent(userEmailContent);
		message.setToEmails(Arrays.asList(user.getEmail()));

		RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
        HttpEntity<EmailMessage> entity = new HttpEntity<>(message, headers);
        //restTemplate.exchange("http://localhost:8096/notification/send", HttpMethod.POST, entity, Void.class);
        logger.info("Notification Service URL: " + env.getProperty("notification.service.url"));
        restTemplate.exchange(env.getProperty("notification.service.url"), HttpMethod.POST, entity, Void.class);

    }
    
    
	@GetMapping("/notification-service-info")
    public ResponseEntity<String> fromNotificationService() {

		RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
        HttpEntity<String> entity = new HttpEntity<>(headers);
        logger.info("Notification Service URL: " + env.getProperty("notification.service.info.url"));
        ResponseEntity<String> result = restTemplate.exchange(env.getProperty("notification.service.info.url"), HttpMethod.GET, entity, String.class);
        return result;

    }
		


	@GetMapping("/notification-health-status")
	public String getNotificationStatus() {
    	
    		RestTemplate restTemplate = new RestTemplate();
            HttpHeaders headers = new HttpHeaders();
            headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
            HttpEntity<String> entity = new HttpEntity<>(headers);
            logger.info("Notification Service URL: " + env.getProperty("notification.service.health.url"));
            ResponseEntity<String> result = restTemplate.exchange(env.getProperty("notification.service.health.url"), HttpMethod.GET, entity, String.class);
            String body = result.getBody();
            return body;
        }
        	
	
	@GetMapping("/notification-xray")
	public Map<String, String> getNotificationAppInfo() throws IOException  {
    	
		
            CloseableHttpClient httpclient = HttpClientBuilder.create().build();
            HttpGet httpGet = new HttpGet(env.getProperty("notification.service.xray.url"));
            logger.info("Notification Service XRay URL: " + env.getProperty("notification.service.xray.url"));
            //logger.info("HTTP Get: " + httpGet);
            CloseableHttpResponse response = httpclient.execute(httpGet);
            //logger.info("HTTP Response: " + response);
            try {
              org.apache.http.HttpEntity entity = (org.apache.http.HttpEntity) response.getEntity();
              InputStream inputStream = ((org.apache.http.HttpEntity) entity).getContent();
              ObjectMapper mapper = new ObjectMapper();
              Map<String, String> jsonMap = mapper.readValue(inputStream, Map.class);
              logger.info("JSON Map: " + jsonMap);
              EntityUtils.consume((org.apache.http.HttpEntity) entity);
              return jsonMap;
            } finally {
              response.close();
            }       

        }

	//The below is a bad code, just to demonstrate calling Notification Service via User Management service on ReactJS UI  - Please don't mind. 
	
	@GetMapping("/ns-status")
	@ResponseStatus(HttpStatus.OK)
	public List<UserModel> listAllUsers2() {
		List<User> users = userRepository.findAll();
		List<UserModel> filteredUsers = users.stream().map(u -> {
			UserModel user = new UserModel();
			user.setUsername("Notification Service");
			user.setEmail(u.getEmail());
			user.setRole(u.getAuthorities().stream().findFirst().get().getAuthority());
			user.setEnabled(u.isEnabled());
			user.setFirstname(u.getFirstname());
			user.setLastname(u.getLastname());
			user.setAppversion(getNotificationStatus());
			return user;
		}).collect(Collectors.toList());
		return filteredUsers;
	}
	

}
