package com.stacksimplify.restservices;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import org.springframework.context.annotation.ComponentScan;
//
@SpringBootApplication
@ComponentScan("com.stacksimplify.restservices")
public class SpringbootSecurityInternalApplication extends SpringBootServletInitializer{

	@Override
	protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
		return application.sources(SpringbootSecurityInternalApplication.class);
	}
	
	public static void main(String[] args) {
		SpringApplication.run(SpringbootSecurityInternalApplication.class, args);
	}

}
