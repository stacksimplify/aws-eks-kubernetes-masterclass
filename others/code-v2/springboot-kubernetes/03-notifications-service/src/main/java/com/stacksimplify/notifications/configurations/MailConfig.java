package com.stacksimplify.notifications.configurations;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.JavaMailSenderImpl;

import java.util.Properties;

@Configuration
public class MailConfig {

	@Value("${mail.server.host}")
	private String mailServerHost;

	@Value("${mail.server.port}")
	private int mailServerPort;

	@Value("${mail.server.auth}")
	private String mailServerAuth;

	@Value("${mail.server.username}")
	private String mailUserName;

	@Value("${mail.server.password}")
	private String mailUserPassword;

	@Value("${mail.server.enableTls}")
	private String mailServerEnableTls;

	@Bean
	public JavaMailSender getMailSender() {
		JavaMailSenderImpl mailSender = new JavaMailSenderImpl();

		if (mailServerAuth.equalsIgnoreCase("true")) {
			mailSender.setUsername(mailUserName);
			mailSender.setPassword(mailUserPassword);
		}

		mailSender.setHost(mailServerHost);
		mailSender.setPort(mailServerPort);

		Properties javaMailProperties = new Properties();
		javaMailProperties.put("mail.smtp.starttls.enable", mailServerEnableTls);
		javaMailProperties.put("mail.smtp.auth", mailServerAuth);
		javaMailProperties.put("mail.transport.protocol", "smtp");
		javaMailProperties.put("mail.debug", "true");// Prints out everything on screen
		javaMailProperties.put("mail.smtp.ssl.protocols", "TLSv1.2"); //TLSv1.2 enabled
			
		javaMailProperties.put("mail.smtp.ssl.protocols", "TLSv1.2");
		mailSender.setJavaMailProperties(javaMailProperties);
		return mailSender;
	}
}