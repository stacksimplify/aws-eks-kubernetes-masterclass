package com.stacksimplify.restservices.authorizationserver.configuration;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.WebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@Configuration
public class AuthorizationServerAuthConfig extends WebSecurityConfigurerAdapter {

	@Bean
	public BCryptPasswordEncoder passwordEncoder() {
		return new BCryptPasswordEncoder(4);
	}
	
	
	
	@Bean
	@Override
	public AuthenticationManager authenticationManagerBean() throws Exception {
		return super.authenticationManagerBean();
	}

	@Autowired
	@Qualifier("userDetailsService")
	private UserDetailsService userDetailsService;

	@Override
	protected void configure(AuthenticationManagerBuilder auth) throws Exception {
		auth.authenticationProvider(authenticationProvider());
	}

	@Bean
	public DaoAuthenticationProvider authenticationProvider() {
		DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider();
		authProvider.setUserDetailsService(userDetailsService);
		authProvider.setPasswordEncoder(passwordEncoder());
		return authProvider;
	}


	
	/*
	//Protect APIs  
	@Override
	public void configure(WebSecurity web) throws Exception {
	    web.ignoring().antMatchers("/public/**", "/error**", "/health/**", "/adminuser**", "/actuator**","/favicon.ico");
	}
	*/

	//UnProtected all APIs
	@Override
	public void configure(WebSecurity web) throws Exception {
	    web.ignoring().antMatchers("/public/**", "/error**", "/health/**", "/adminuser**", "/actuator**", 
	    		"/favicon.ico", "/usermgmt/**", "/notification-xray**", "/notification-service-info**", "/ns-status**","/notification-health-status**", "/health-status**","/users**", "/user**", "/user/**", "/status/**", "/h2-console/**", "/hello**", "/app1/**", "/app2/**");
	}
	
	
}













