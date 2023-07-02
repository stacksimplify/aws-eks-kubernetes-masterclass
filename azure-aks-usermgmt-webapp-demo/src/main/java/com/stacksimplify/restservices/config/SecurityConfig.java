package com.stacksimplify.restservices.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

//@Configuration
//@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

	@Autowired
	private BCryptPasswordEncoder passwordEncoder;

	//Define Static User
	@Override
	protected void configure(AuthenticationManagerBuilder auth) throws Exception {

		auth.inMemoryAuthentication()
			.withUser("admin")
			.password(passwordEncoder.encode("admin"))
			.roles("ADMIN");
		
		auth.inMemoryAuthentication()
		.withUser("user")
		.password(passwordEncoder.encode("user"))
		.roles("USER");
	}

	//Protection for All API's
	/*@Override
	protected void configure(HttpSecurity http) throws Exception {
		http.csrf().disable();
		http.authorizeRequests()
			.anyRequest()
			.fullyAuthenticated()
			.and()
			.httpBasic();
	}*/
	
	//Protection based on URI's
	/*@Override
	protected void configure(HttpSecurity http) throws Exception {
		http.csrf().disable();
		http.authorizeRequests()
		.antMatchers("/users/**")
		.fullyAuthenticated()
		.and()
		.httpBasic();
		
	}*/
	
	//Protection based on ROLES
	@Override
	protected void configure(HttpSecurity http) throws Exception {
		http.csrf().disable();
		http.authorizeRequests()
		.antMatchers("/users**")
		.hasAnyRole("ADMIN")
		.anyRequest()
		.fullyAuthenticated()
		.and()
		.httpBasic();
		
	}
		
/*
	//Define the simple BCryptPasswordEncoder as a bean in our configuration
	@Bean
	public PasswordEncoder passwordEncoder() {
		return new BCryptPasswordEncoder();
	}
	
*/	
	// Define the simple BCryptPasswordEncoder as a bean in our configuration
	@Bean
	public BCryptPasswordEncoder passwordEncoder() {
		return new BCryptPasswordEncoder();
	}
	

}
